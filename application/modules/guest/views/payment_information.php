<!DOCTYPE html>

<!--[if lt IE 7]>
<html class="no-js ie6 oldie" lang="<?php _trans('cldr'); ?>"> <![endif]-->
<!--[if IE 7]>
<html class="no-js ie7 oldie" lang="<?php _trans('cldr'); ?>"> <![endif]-->
<!--[if IE 8]>
<html class="no-js ie8 oldie" lang="<?php _trans('cldr'); ?>"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class="no-js" lang="<?php _trans('cldr'); ?>"> <!--<![endif]-->

<head>
    <title><?php echo get_setting('custom_title', 'InvoicePlane', true); ?></title>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="robots" content="NOINDEX,NOFOLLOW">
    <meta name="_csrf" content="<?php echo $this->security->get_csrf_hash() ?>">
    <meta name="csrf_token_name" content="<?php echo config_item('csrf_token_name'); ?>">
    <meta name="csrf_cookie_name" content="<?php echo config_item('csrf_cookie_name'); ?>">
    <meta name="legacy_calculation" content="<?php echo (int) (config_item('legacy_calculation')); ?>">

    <link rel="icon" href="<?php _core_asset('img/favicon.png'); ?>" type="image/png">

    <link rel="stylesheet" href="<?php _theme_asset('css/style.css'); ?>" type="text/css">
    <link rel="stylesheet" href="<?php _core_asset('css/custom.css'); ?>" type="text/css">

<?php if (get_setting('monospace_amounts') == 1) { ?>
    <link rel="stylesheet" href="<?php _theme_asset('css/monospace.css'); ?>" type="text/css">
<?php } ?>

    <!--[if lt IE 9]>
    <script src="<?php _core_asset('js/legacy.min.js'); ?>"></script>
    <![endif]-->

    <script src="<?php _core_asset('js/dependencies.min.js'); ?>"></script>

</head>
<body>

<nav class="navbar navbar-default ">
    <div class="container">

        <div class="navbar-brand">
            <?php _trans('online_payment_for_invoice'); ?> #<?php echo $invoice->invoice_number; ?>
        </div>

        <ul class="nav navbar-nav navbar-right">
            <li>
                <a target="_blank" href="<?php echo site_url('guest/view/generate_invoice_pdf/' . $invoice->invoice_url_key); ?>">
                    <i class="fa fa-print"></i> <?php _trans('download_pdf'); ?>
                </a>
            </li>
        </ul>

    </div>
</nav>

<div class="container">

    <div class="row">
        <div class="col-xs-12 col-md-8 col-md-offset-2">

            <br>
<?php
            $logo = invoice_logo();
            if ($logo) {
                echo $logo . '<br><br>';
            }
?>

            <div class="form-group">
                <?php echo $this->layout->load_view('layout/alerts', ['without_margin' => true]); ?>
            </div>

            <div class="panel panel-default">

                <div class="panel-body">

                    <div class="row">
                        <div class="col-xs-12 col-md-7">
                            <h4>
                                <?php _htmlsc(format_client($invoice)) ?>
                            </h4>
                            <div class="client-address">
<?php $this->layout->load_view('clients/partial_client_address', ['client' => $invoice]); ?>
                            </div>
                        </div>

                        <div class="col-xs-12 col-md-5">
                            <div class="hidden-md hidden-lg"><br></div>
                            <div class="table-responsive">
                                <table class="table table-bordered table-condensed no-margin">
                                    <tbody>
                                        <tr>
                                            <td><?php echo trans('invoice_date'); ?></td>
                                            <td class="text-right"><?php echo date_from_mysql($invoice->invoice_date_created); ?></td>
                                        </tr>
                                        <tr class="<?php echo $is_overdue ? 'overdue' : '' ?>">
                                            <td><?php echo trans('due_date'); ?></td>
                                            <td class="text-right">
                                                <?php echo date_from_mysql($invoice->invoice_date_due); ?>
                                            </td>
                                        </tr>
                                        <tr class="<?php echo $is_overdue ? 'overdue' : '' ?>">
                                            <td><?php echo trans('total'); ?></td>
                                            <td class="text-right"><?php echo format_currency($invoice->invoice_total); ?></td>
                                        </tr>
                                        <tr class="<?php echo $is_overdue ? 'overdue' : '' ?>">
                                            <td><?php echo trans('balance'); ?></td>
                                            <td class="text-right"><?php echo format_currency($invoice->invoice_balance); ?></td>
                                        </tr>
<?php
if ($payment_method) {
?>
                                        <tr>
                                            <td><?php echo trans('payment_method') . ': '; ?></td>
                                            <td class="text-right"><?php _htmlsc($payment_method->payment_method_name); ?></td>
                                        </tr>
<?php
}
?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
<?php
if ( ! empty($invoice->invoice_terms)) {
?>
                        <div class="col-xs-12 text-muted">
                            <br>
                            <h4><?php _trans('terms'); ?></h4>
                            <div><?php _htmlsc(nl2br($invoice->invoice_terms)); ?></div>
                        </div>
<?php
}
?>
                    </div>

                </div>
            </div>
<?php
if ($payment_provider == null && ! $disable_form) {
?>
                <div>
                    <p><?php echo trans('select_payment_method'); ?></p>
                </div>
                <ul class="list-group">
<?php
    foreach ($gateways as $gateway) {
?>
                    <a class="list-group-item list-group-item-action" href="<?php echo site_url('guest/payment_information/form/' . $invoice->invoice_url_key . '/' . $gateway); ?>"><?php echo ucwords(str_replace('_', ' ', $gateway)); ?></a>
<?php
    }
?>
                </ul>
<?php
}
?>
        </div>
    </div>

</div>

<div id="modal-placeholder"></div>

<?php echo $this->layout->load_view('layout/includes/fullpage-loader'); ?>

<script defer src="<?php _core_asset('js/scripts.min.js'); ?>"></script>
</body>
</html>
