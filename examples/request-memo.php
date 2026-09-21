<?php
require __DIR__.'/RequestMemo.php';
$calls=0;
$memo=new RequestMemo;
$loader=function () use (&$calls) { $calls++; return null; };
for ($i=0;$i<100;$i++) {
    if ($memo->read('display-title', 'default', $loader) !== null) throw new RuntimeException('Null changed');
}
if ($calls!==1) throw new RuntimeException('Repeated work');
$memo->forget('display-title');
if ($memo->read('display-title', 'default', fn ()=>'updated') !== 'updated') throw new RuntimeException('Stale value');
$next=new RequestMemo;
if ($next->read('display-title', 'default', fn ()=>'next request') !== 'next request') throw new RuntimeException('Lifecycle leak');
$attempts=0;
try { $next->read('temporary-failure', null, function () use (&$attempts) { $attempts++; throw new RuntimeException('expected'); }); } catch (RuntimeException) {}
$next->read('temporary-failure', null, function () use (&$attempts) { $attempts++; return 'recovered'; });
if ($attempts!==2) throw new RuntimeException('Failure was cached');
echo "Synthetic memo contract passed: repeated reads, null, invalidation, new lifecycle, failure recovery.\n";
