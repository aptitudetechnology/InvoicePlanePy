<div id="headerbar">
    <h1 class="headerbar-title"><?php _trans('dashboard'); ?></h1>
</div>

<div id="content">

    <?php echo $this->layout->load_view('layout/alerts'); ?>

    <div class="panel panel-default">

        <div class="panel-heading"><?php _trans('quotes_requiring_approval'); ?></div>

        <div class="panel-body no-padding">

<?php
if ($open_quotes) {
    echo $this->layout->load_view('guest/partial_quotes_table', ['quotes' => $open_quotes]);
} else {
?>
            <div class="alert text-success no-margin"><?php _trans('no_quotes_requiring_approval'); ?></div>
<?php
}
?>

        </div>
    </div>

    <div class="panel panel-default">
        <div class="panel-heading"><?php _trans('overdue_invoices'); ?></div>
        <div class="panel-body no-padding">
<?php
if ($overdue_invoices) {
    echo $this->layout->load_view('guest/partial_invoices_table', ['invoices' => $overdue_invoices]);
} else {
?>
            <div class="alert text-success no-margin"><?php _trans('no_overdue_invoices'); ?></div>
<?php
}
?>

        </div>
    </div>

    <div class="panel panel-default">

        <div class="panel-heading"><?php _trans('open_invoices'); ?></div>

        <div class="panel-body no-padding">

<?php
if ($overdue_invoices) {
    echo $this->layout->load_view('guest/partial_invoices_table', ['invoices' => $open_invoices]);
} else {
?>
            <div class="alert text-success no-margin"><?php _trans('no_open_invoices'); ?></div>
<?php
}
?>

        </div>

    </div>

</div>
