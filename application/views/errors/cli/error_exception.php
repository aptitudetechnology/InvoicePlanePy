<?php defined('BASEPATH') || exit('No direct script access allowed'); ?>

An uncaught Exception was encountered

Type:        <?php echo get_class($exception), "\n"; ?>
Message:     <?php echo $message, "\n"; ?>
Filename:    <?php echo $exception->getFile(), "\n"; ?>
Line Number: <?php echo $exception->getLine(); ?>

<?php if (defined('SHOW_DEBUG_BACKTRACE') && SHOW_DEBUG_BACKTRACE) : ?>
    Backtrace:
    <?php foreach ($exception->getTrace() as $error) : ?>
        <?php if (isset($error['file']) && ! str_starts_with($error['file'], realpath(BASEPATH))) : ?>
            File: <?php echo $error['file'], "\n"; ?>
            Line: <?php echo $error['line'], "\n"; ?>
            Function: <?php echo $error['function'], "\n\n"; ?>
        <?php endif ?>
    <?php endforeach ?>

<?php endif;
