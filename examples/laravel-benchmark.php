<?php
// All data is synthetic. No application boot, network calls, or production configuration.
// Usage: php examples/laravel-benchmark.php /path/to/vendor/autoload.php /tmp/benchmark-output
if ($argc !== 3 || !is_file($argv[1])) {
    fwrite(STDERR, "Pass a Composer autoloader and a new output directory.\n"); exit(2);
}
require $argv[1];
require __DIR__.'/RequestMemo.php';
use Illuminate\Container\Container;
use Illuminate\Database\SQLiteConnection;
use Illuminate\Cache\DatabaseStore;
use Illuminate\Cache\Repository;
if (is_dir($argv[2])) { fwrite(STDERR, "Output directory must be new.\n"); exit(2); }
mkdir($argv[2], 0700, true);
$pdo = new PDO('sqlite::memory:');
$db = new SQLiteConnection($pdo);
$db->statement('CREATE TABLE cache (key TEXT PRIMARY KEY, value TEXT NOT NULL, expiration INTEGER NOT NULL)');
$cache = new Repository(new DatabaseStore($db, 'cache', 'synthetic:'));
$cache->put('currency', 'GBP', 3600);
$container = new Container;
$container->scoped(RequestMemo::class);
$context = ['dataset'=>'one-synthetic-currency-2000-reads-v1','clock'=>'fixed-input-no-date-logic','runtime'=>PHP_VERSION.';cli;opcache='.(ini_get('opcache.enable_cli') ?: '0'), 'database'=>'sqlite:'. $pdo->query('select sqlite_version()')->fetchColumn(), 'role'=>'synthetic-no-authorization','cache_state'=>'warm-database-cache','concurrency'=>'1','measurement'=>'synthetic-server-processing'];
foreach (['baseline', 'candidate'] as $variant) {
    $samples=[];
    for ($sample=0; $sample<7; $sample++) {
        $container->forgetScopedInstances();
        $db->flushQueryLog(); $db->enableQueryLog();
        $result=[]; $start=hrtime(true);
        for ($i=0; $i<2000; $i++) {
            $result[] = $variant==='baseline'
                ? $cache->get('currency', 'USD')
                : $container->make(RequestMemo::class)->read('currency', 'USD', fn ()=>$cache->get('currency', 'USD'));
        }
        $ms=(hrtime(true)-$start)/1e6;
        $queries=count($db->getQueryLog()); $db->disableQueryLog();
        if ($sample) $samples[]=['case'=>'repeated-setting','duration_ms'=>$ms,'queries'=>$queries,'status'=>200,'result_hash'=>hash('sha256',json_encode($result,JSON_THROW_ON_ERROR))];
    }
    file_put_contents($argv[2].'/'.$variant.'.json',json_encode(['context'=>$context,'samples'=>$samples],JSON_PRETTY_PRINT|JSON_THROW_ON_ERROR));
}
echo "Synthetic benchmark written. Compare both JSON files with scripts/compare.py.\n";
