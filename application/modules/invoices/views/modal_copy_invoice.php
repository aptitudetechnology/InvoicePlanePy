<script>
    $(function () {
        // Display the copy invoice modal
        $('#modal_copy_invoice').modal('show');

        // Select2 for all select inputs
        $(".simple-select").select2();

        <?php $this->layout->load_view('clients/script_select2_client_id.js'); ?>

        // Creates the invoice
        $('#copy_invoice_confirm').click(function () {
            show_loader(); // Show spinner
            $.post("<?php echo site_url('invoices/ajax/copy_invoice'); ?>", {
                    invoice_id: <?php echo $invoice_id; ?>,
                    client_id: $('#client_id').val(),
                    user_id: $('#user_id').val(),
                    invoice_date_created: $('#invoice_date_created_modal').val(),
                    invoice_group_id: $('#invoice_group_id').val(),
                    invoice_password: $('#invoice_password').val(),
                    invoice_time_created: '<?php echo date('H:i:s') ?>',
                    payment_method: $('#payment_method').val()
                },
                function (data) {
                    var response = json_parse(data, <?php echo (int) IP_DEBUG; ?>);
                    if (response.success === 1) {
                        window.location = "<?php echo site_url('invoices/view'); ?>/" + response.invoice_id;
                    }
                    else {
                        // The validation was not successful
                        close_loader();
                        $('.control-group').removeClass('has-error');
                        for (var key in response.validation_errors) {
                            $('#' + key).parent().parent().addClass('has-error');
                        }
                    }
                }
            );
        });
    });

</script>

<div id="modal_copy_invoice" class="modal modal-lg" role="dialog" aria-labelledby="modal_copy_invoice"
     aria-hidden="true">
    <form class="modal-content">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"><i class="fa fa-close"></i></button>
            <h4 class="panel-title"><?php _trans('copy_invoice'); ?></h4>
        </div>
        <div class="modal-body">

            <input type="hidden" name="user_id" id="user_id" value="<?php echo $invoice->user_id; ?>">
            <input type="hidden" name="payment_method" id="payment_method" class="form-control"
                   value="<?php echo $invoice->payment_method; ?>">
            <input class="hidden" id="input_permissive_search_clients"
                   value="<?php echo get_setting('enable_permissive_search_clients'); ?>">

            <div class="form-group has-feedback">
                <label for="client_id"><?php _trans('client'); ?></label>
                <div class="input-group">
                    <span id="toggle_permissive_search_clients" class="input-group-addon" title="<?php _trans('enable_permissive_search_clients'); ?>" style="cursor:pointer;">
                        <i class="fa fa-toggle-<?php echo get_setting('enable_permissive_search_clients') ? 'on' : 'off' ?> fa-fw" ></i>
                    </span>
                    <select name="client_id" id="client_id" class="client-id-select form-control" autofocus="autofocus" required="required">
<?php if ( ! empty($client)) : ?>
                        <option value="<?php echo $client->client_id; ?>"><?php _htmlsc(format_client($client, false)); ?></option>
<?php endif; ?>
                    </select>
                </div>
            </div>

            <div class="form-group has-feedback">
                <label for="invoice_date_created_modal"><?php _trans('invoice_date'); ?>: </label>

                <div class="input-group">
                    <input name="invoice_date_created_modal" id="invoice_date_created_modal" class="form-control datepicker"
                           value="<?php echo date_from_mysql(date('Y-m-d', time()), true) ?>">
                    <span class="input-group-addon">
                        <i class="fa fa-calendar fa-fw"></i>
                    </span>
                </div>
            </div>

            <div class="form-group">
                <label for="invoice_password"><?php _trans('invoice_password'); ?></label>
                <input type="text" name="invoice_password" id="invoice_password" class="form-control"
                       value="<?php echo get_setting('invoice_pre_password') == '' ? '' : get_setting('invoice_pre_password') ?>"
                       style="margin: 0 auto;" autocomplete="off">
            </div>

            <div class="form-group">
                <label for="invoice_group_id"><?php _trans('invoice_group'); ?>: </label>
                <select name="invoice_group_id" id="invoice_group_id" class="form-control simple-select">
                    <?php foreach ($invoice_groups as $invoice_group) { ?>
                        <option value="<?php echo $invoice_group->invoice_group_id; ?>"
                            <?php check_select(get_setting('default_invoice_group'), $invoice_group->invoice_group_id); ?>>
                            <?php _htmlsc($invoice_group->invoice_group_name); ?>
                        </option>
                    <?php } ?>
                </select>
            </div>

        </div>

        <div class="modal-footer">
            <div class="btn-group">
                <button class="btn btn-success" id="copy_invoice_confirm" type="button">
                    <i class="fa fa-check"></i> <?php _trans('submit'); ?>
                </button>
                <button class="btn btn-danger" type="button" data-dismiss="modal">
                    <i class="fa fa-times"></i> <?php _trans('cancel'); ?>
                </button>
            </div>
        </div>

    </form>

</div>
