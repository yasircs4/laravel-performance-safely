<?php
// Synthetic standalone contract example. Register this kind of object as scoped
// in Laravel, and preserve your real settings service's decoding/error behavior.
final class RequestMemo
{
    private array $entries = [];
    public function read(string $key, mixed $default, Closure $loader): mixed
    {
        foreach ($this->entries[$key] ?? [] as [$previousDefault, $value]) {
            if ($previousDefault === $default) return $value;
        }
        $value = $loader();
        $this->entries[$key][] = [$default, $value];
        return $value;
    }
    public function forget(string $key): void { unset($this->entries[$key]); }
}
