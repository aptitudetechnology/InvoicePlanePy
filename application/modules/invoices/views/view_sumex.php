<?php
if ($this->config->item('disable_read_only') == true) {
    $invoice->is_read_only = 0;
}
// Little helper
$its_mine = $this->session->__get('user_id') == $invoice->user_id;
$my_class = $its_mine ? 'success' : 'warning'; // visual: work with text-* alert-*
// In change user toggle & After eInvoice (name) when user required field missing
$edit_user_title = trans('edit') . ' ' . trans('user') . ' (' . trans('invoicing') . '): ' . htmlsc(PHP_EOL . format_user($invoice->user_id));
?>
<script>
    $(function () {
        $('.item-task-id').each(function () {
            // Disable client change if at least one item already has a task id assigned
            if ($(this).val().length > 0) {
                $('#invoice_change_client').hide();
                return false;
            }
        });

        $('.btn_add_product').click(function () {
            $('#modal-placeholder').load("<?php echo site_url('products/ajax/modal_product_lookups'); ?>/" + Math.floor(Math.random() * 1000));
        });

        $('.btn_add_task').click(function () {
            $('#modal-placeholder').load("<?php echo site_url('tasks/ajax/modal_task_lookups/' . $invoice_id); ?>/" + Math.floor(Math.random() * 1000));
        });

        $('.btn_add_row').click(function () {
            $('#new_row').clone().appendTo('#item_table').removeAttr('id').addClass('item').show();
            // Legacy:no: check items tax usage is correct (ReLoad on change)
            check_items_tax_usages();
        });

<?php
if ( ! $items) {
    ?>
        $('#new_row').clone().appendTo('#item_table').removeAttr('id').addClass('item').show();
<?php
}
?>

        // Legacy:no: check items tax usage is correct (Load on change)
        $(document).on('loaded', check_items_tax_usages());

        $('#btn_create_recurring').click(function () {
            $('#modal-placeholder').load(
                "<?php echo site_url('invoices/ajax/modal_create_recurring'); ?>",
                {
                    invoice_id: <?php echo $invoice_id; ?>
                }
            );
        });

        $('#invoice_change_client').click(function () {
            $('#modal-placeholder').load("<?php echo site_url('invoices/ajax/modal_change_client'); ?>", {
                invoice_id: <?php echo $invoice_id; ?>,
                client_id: "<?php echo $this->db->escape_str($invoice->client_id); ?>"
            });
        });

        $('#btn_save_invoice').click(function () {
            var items = [];
            var item_order = 1;
            $('#item_table .item').each(function () {
                var row = {};
                $(this).find('input,select,textarea').each(function () {
                    if ($(this).is(':checkbox')) {
                        row[$(this).attr('name')] = $(this).is(':checked');
                    } else {
                        row[$(this).attr('name')] = $(this).val();
                    }
                });
                row['item_order'] = item_order;
                item_order++;
                items.push(row);
            });
            $.post("<?php echo site_url('invoices/ajax/save'); ?>", {
                    invoice_id: <?php echo $invoice_id; ?>,
                    invoice_number: $('#invoice_number').val(),
                    invoice_date_created: $('#invoice_date_created').val(),
                    invoice_date_due: $('#invoice_date_due').val(),
                    invoice_status_id: $('#invoice_status_id').val(),
                    invoice_password: $('#invoice_password').val(),
                    invoice_sumex_reason: $("#invoice_sumex_reason").val(),
                    invoice_sumex_treatmentstart: $("#invoice_sumex_treatmentstart").val(),
                    invoice_sumex_treatmentend: $("#invoice_sumex_treatmentend").val(),
                    invoice_sumex_casedate: $("#invoice_sumex_casedate").val(),
                    invoice_sumex_casenumber: $("#invoice_sumex_casenumber").val(),
                    invoice_sumex_diagnosis: $("#invoice_sumex_diagnosis").val(),
                    invoice_sumex_observations: $("#invoice_sumex_observations").val(),
                    items: JSON.stringify(items),
                    invoice_discount_amount: $('#invoice_discount_amount').val(),
                    invoice_discount_percent: $('#invoice_discount_percent').val(),
                    invoice_terms: $('#invoice_terms').val(),
                    custom: $('input[name^=custom],select[name^=custom]').serializeArray(),
                    payment_method: $('#payment_method').val()
                },
                function (data) {
                    var response = json_parse(data, <?php echo (int) IP_DEBUG; ?>);
                    if (response.success === 1) {
                        window.location = "<?php echo site_url('invoices/view'); ?>/" + <?php echo $invoice_id; ?>;
                    } else {
                        $('#fullpage-loader').hide();
                        $('.control-group').removeClass('has-error');
                        $('div.alert[class*="alert-"]').remove();
                        var resp_errors = response.validation_errors,
                            all_resp_errors = '';
                        for (var key in resp_errors) {
                            $('#' + key).parent().addClass('has-error');
                            all_resp_errors += resp_errors[key];
                        }
                        $('#invoice_form').prepend('<div class="alert alert-danger">' + all_resp_errors + '</div>');
                    }
                });
        });

        $('#btn_generate_pdf').click(function () {
            window.open('<?php echo site_url('invoices/generate_sumex_copy/' . $invoice_id); ?>', '_blank');
        });

        $('#btn_sumex').click(function () {
            window.open('<?php echo site_url('invoices/generate_sumex_pdf/' . $invoice_id); ?>', '_blank');
        });

        $(document).on('click', '.btn_delete_item', function () {
            var btn = $(this);
            var item_id = btn.data('item-id');

            // Just remove the row if no item ID is set (new row)
            if (typeof item_id === 'undefined') {
                $(this).parents('.item').remove();
                check_items_tax_usages();
            } else {
                $.post("<?php echo site_url('invoices/ajax/delete_item/' . $invoice->invoice_id); ?>", {
                        'item_id': item_id,
                    },
                    function (data) {
                        var response = json_parse(data, <?php echo (int) IP_DEBUG; ?>);
                        if (response.success === 1) {
                            btn.parents('.item').remove();
                        } else {
                            btn.removeClass('btn-link').addClass('btn-danger').prop('disabled', true);
                        }

                        check_items_tax_usages();
                    }
                );
            }
        });

<?php
if ($invoice->is_read_only != 1) {
?>
        var fixHelper = function (e, tr) {
            var $originals = tr.children();
            var $helper = tr.clone();
            $helper.children().each(function (index) {
                $(this).width($originals.eq(index).width())
            });
            return $helper;
        };

        $("#item_table").sortable({
            items: 'tbody',
            helper: fixHelper
        });

        $(document).ready(function () {
            if ($('#invoice_discount_percent').val().length > 0) {
                $('#invoice_discount_amount').prop('disabled', true);
            }
            if ($('#invoice_discount_amount').val().length > 0) {
                $('#invoice_discount_percent').prop('disabled', true);
            }
        });
        $('#invoice_discount_amount').keyup(function () {
            if (this.value.length > 0) {
                $('#invoice_discount_percent').prop('disabled', true);
            } else {
                $('#invoice_discount_percent').prop('disabled', false);
            }
        });
        $('#invoice_discount_percent').keyup(function () {
            if (this.value.length > 0) {
                $('#invoice_discount_amount').prop('disabled', true);
            } else {
                $('#invoice_discount_amount').prop('disabled', false);
            }
        });
<?php
}
?>
    });
</script>

<?php
echo $modal_delete_invoice;
echo $legacy_calculation ? $modal_add_invoice_tax : ''; // Legacy calculation have global taxes - since v1.6.3
?>

<div id="headerbar">
    <h1 class="headerbar-title">
        <span data-toggle="tooltip" data-placement="bottom" title="<?php _trans('invoicing'); ?>: <?php _htmlsc(PHP_EOL . format_user($invoice->user_id)); ?>">
            <?php echo trans('invoice') . ' ' . ($invoice->invoice_number ? '#' . $invoice->invoice_number : trans('id') . ': ' . $invoice->invoice_id); ?>
        </span>
<?php
// Nb Admins > 1 only
if ($change_user) {
?>
        <a data-toggle="tooltip" data-placement="bottom"
           title="<?php echo $edit_user_title; ?>"
           href="<?php echo site_url('users/form/' . $invoice->user_id); ?>">
            <i class="fa fa-xs fa-user text-<?php echo $my_class; ?>"></i>
                <span class="hidden-xs"><?php _htmlsc($invoice->user_name); ?></span>
        </a>
<?php
    if ($invoice->invoice_status_id == 1 && ! $invoice->creditinvoice_parent_id) {
?>

        <span id="invoice_change_user" class="fa fa-fw fa-edit text-<?php echo $its_mine ? 'muted' : 'danger'; ?> cursor-pointer"
              data-toggle="tooltip" data-placement="bottom"
              title="<?php _trans('change_user'); ?>"></span>
<?php
    } // End if draft
} // End if change_user
?>
    </h1>

    <div class="headerbar-item pull-right<?php echo ($invoice->is_read_only != 1 || $invoice->invoice_status_id != 4) ? ' btn-group' : ''; ?>">

        <div class="options btn-group pull-left">
            <a class="btn btn-sm btn-default dropdown-toggle"
               data-toggle="dropdown" href="#">
                <i class="fa fa-caret-down no-margin"></i> <?php _trans('options'); ?>
            </a>
            <ul class="dropdown-menu">
<?php
if ($legacy_calculation && $invoice->is_read_only != 1) { // Legacy calculation have global taxes - since v1.6.3
?>
                <li>
                    <a href="#add-invoice-tax" data-toggle="modal">
                        <i class="fa fa-plus fa-margin"></i> <?php _trans('add_invoice_tax'); ?>
                    </a>
                </li>
<?php
}
?>
                <li>
                    <a href="#" id="btn_create_credit" data-invoice-id="<?php echo $invoice_id; ?>">
                        <i class="fa fa-minus fa-margin"></i> <?php _trans('create_credit_invoice'); ?>
                    </a>
                </li>
<?php
if ($invoice->invoice_balance != 0) {
?>
                <li>
                    <a href="#" class="invoice-add-payment"
                       data-invoice-id="<?php echo $invoice_id; ?>"
                       data-invoice-balance="<?php echo $invoice->invoice_balance; ?>"
                       data-invoice-payment-method="<?php echo $invoice->payment_method; ?>"
                       data-payment-cf-exist="<?php echo $payment_cf_exist ?? ''; ?>">
                        <i class="fa fa-credit-card fa-margin"></i>
                        <?php _trans('enter_payment'); ?>
                    </a>
                </li>
<?php
}
?>
                <li>
                    <a href="#" id="btn_generate_pdf"
                       data-invoice-id="<?php echo $invoice_id; ?>">
                        <i class="fa fa-file-text fa-margin"></i>
                        <?php _trans('generate_copy'); ?>
                    </a>
                </li>
                <li>
                    <a href="#" id="btn_sumex"
                       data-invoice-id="<?php echo $invoice_id; ?>">
                        <i class="fa fa-user-md fa-margin"></i>
                        <?php _trans('generate_sumex'); ?>
                    </a>
                </li>
                <li>
                    <a href="<?php echo site_url('mailer/invoice/' . $invoice->invoice_id); ?>">
                        <i class="fa fa-send fa-margin"></i>
                        <?php _trans('send_email'); ?>
                    </a>
                </li>
                <li class="divider"></li>
                <li>
                    <a href="#" id="btn_create_recurring"
                       data-invoice-id="<?php echo $invoice_id; ?>">
                        <i class="fa fa-repeat fa-margin"></i>
                        <?php _trans('create_recurring'); ?>
                    </a>
                </li>
                <li>
                    <a href="#" id="btn_copy_invoice"
                       data-invoice-id="<?php echo $invoice_id; ?>">
                        <i class="fa fa-copy fa-margin"></i>
                        <?php _trans('copy_invoice'); ?>
                    </a>
                </li>
<?php
if ($invoice->invoice_status_id == 1 || ($this->config->item('enable_invoice_deletion') === true && $invoice->is_read_only != 1)) {
?>
                <li>
                    <a href="#delete-invoice" data-toggle="modal">
                        <i class="fa fa-trash-o fa-margin"></i>
                        <?php _trans('delete'); ?>
                    </a>
                </li>
<?php
}
?>
            </ul>
        </div>

<?php
if ($invoice->is_read_only != 1 || $invoice->invoice_status_id != 4) {
?>
        <a href="#" class="btn btn-sm btn-success ajax-loader" id="btn_save_invoice">
            <i class="fa fa-check"></i> <?php _trans('save'); ?>
        </a>
<?php
}
?>
    </div>

    <div class="headerbar-item invoice-labels pull-right">
<?php
if ($invoice->invoice_is_recurring) {
?>
        <span class="label label-info"><?php _trans('recurring'); ?></span>
<?php
}
if ($invoice->is_read_only == 1) {
?>
        <span class="label label-danger">
            <i class="fa fa-read-only"></i> <?php _trans('read_only'); ?>
        </span>
<?php
}
?>
    </div>

</div>

<div id="content">

    <?php echo $this->layout->load_view('layout/alerts'); ?>

    <div id="invoice_form">
        <div class="invoice">
            <div class="cf row">
                <div class="col-xs-12 col-md-8">
                    <div class="col-md-6">
                        <h2>
                            <a href="<?php echo site_url('clients/view/' . $invoice->client_id); ?>"><?php echo format_client($invoice) ?></a>
<?php
if ($invoice->invoice_status_id == 1) {
?>
                                <span id="invoice_change_client" class="fa fa-edit cursor-pointer small"
                                      data-toggle="tooltip" data-placement="bottom"
                                      title="<?php echo htmlentities(trans('change_client'), ENT_COMPAT); ?>"></span>
<?php
}
?>
                        </h2><br>
                        <span>
                            <?php echo ($invoice->client_address_1) ? $invoice->client_address_1 . '<br>' : ''; ?>
                            <?php echo ($invoice->client_address_2) ? $invoice->client_address_2 . '<br>' : ''; ?>
                            <?php echo ($invoice->client_city) ? $invoice->client_city : ''; ?>
                            <?php echo ($invoice->client_state) ? $invoice->client_state : ''; ?>
                            <?php echo ($invoice->client_zip) ? $invoice->client_zip : ''; ?>
                            <?php echo ($invoice->client_country) ? '<br>' . $invoice->client_country : ''; ?>
                        </span>
<?php if ($invoice->client_phone || $invoice->client_email) : ?>
                            <hr>
<?php endif; ?>
<?php if ($invoice->client_phone) : ?>
                            <div><?php _trans('phone'); ?>:&nbsp;<?php _htmlsc($invoice->client_phone); ?></div>
<?php endif; ?>
<?php if ($invoice->client_email) : ?>
                            <div><?php _trans('email'); ?>:&nbsp;<?php _auto_link($invoice->client_email); ?></div>
<?php endif; ?>
<?php if ($invoice->client_birthdate || $invoice->client_gender) : ?>
                            <hr>
<?php endif; ?>
<?php if ($invoice->client_birthdate) : ?>
                            <div><?php _trans('birthdate'); ?>:&nbsp;<?php echo format_date($invoice->client_birthdate); ?></div>
<?php endif; ?>
<?php if ($invoice->client_gender) : ?>
                            <div><?php _trans('birthdate'); ?>:&nbsp;<?php echo format_gender($invoice->client_gender); ?></div>
<?php endif; ?>
                    </div>
                    <div class="col-md-6">
<?php
// Fix New invoice date in db
$invoice->sumex_treatmentstart = $invoice->sumex_treatmentstart == '0000-00-00' ? date('y-m-d') : $invoice->sumex_treatmentstart;
$invoice->sumex_treatmentend   = $invoice->sumex_treatmentend   == '0000-00-00' ? date('y-m-d') : $invoice->sumex_treatmentend;
$invoice->sumex_casedate       = $invoice->sumex_casedate       == '0000-00-00' ? date('y-m-d') : $invoice->sumex_casedate;
?>
                        <h3><?php _trans('treatment'); ?></h3>
                        <br>
                        <div class="col-xs-12 col-md-8">
                            <table class="items table">
                                <tr>
                                    <td>
                                        <div class="input-group">
                                            <span class="input-group-addon"><?php _trans('start'); ?></span>
                                            <input id="invoice_sumex_treatmentstart" name="sumex_treatmentstart"
                                                   class="form-control datepicker"
                                                   value="<?php echo date_from_mysql($invoice->sumex_treatmentstart); ?>"
                                                   type="text">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div class="input-group">
                                            <span class="input-group-addon"><?php _trans('end'); ?></span>
                                            <input id="invoice_sumex_treatmentend" name="sumex_treatmentend"
                                                   class="form-control datepicker"
                                                   value="<?php echo date_from_mysql($invoice->sumex_treatmentend); ?>"
                                                   type="text">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div class="input-group">
                                            <span class="input-group-addon"><?php _trans('reason'); ?></span>
                                            <select name="invoice_sumex_reason" id="invoice_sumex_reason"
                                                    class="form-control simple-select">
<?php
$reasons = [
    'accident',
    'birthdefect',
    'disease',
    'maternity',
    'prevention',
    'unknown',
];
foreach ($reasons as $key => $reason) {
    $selected = ($invoice->sumex_reason == $key ? ' selected' : '');
?>
                                                <option value="<?php echo $key; ?>"<?php echo $selected; ?>>
                                                    <?php _trans('reason_' . $reason); ?>
                                                </option>
<?php
} // End foreach
?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div class="input-group">
                                            <span class="input-group-addon"><?php _trans('case_date'); ?></span>
                                            <input id="invoice_sumex_casedate" name="sumex_casedate"
                                                   class="form-control datepicker"
                                                   value="<?php echo date_from_mysql($invoice->sumex_casedate); ?>"
                                                   type="text">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div class="input-group">
                                            <span class="input-group-addon"><?php _trans('case_number'); ?></span>
                                            <input id="invoice_sumex_casenumber" name="sumex_casenumber"
                                                   class="form-control"
                                                   value="<?php _htmle($invoice->sumex_casenumber); ?>"
                                                   type="text">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <div class="input-group">
                                            <span class="input-group-addon"><?php _trans('invoice_sumex_diagnosis'); ?></span>
                                            <input id="invoice_sumex_diagnosis" name="invoice_sumex_diagnosis"
                                                   class="form-control"
                                                   value="<?php _htmle($invoice->sumex_diagnosis); ?>"
                                                   type="text" maxlength="500">
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </div>

                <div class="col-xs-12 col-md-4">

                    <div class="details-box">

                        <div class=" row">

<?php
if ($invoice->invoice_sign == -1) {
    $credit_link = anchor('/invoices/view/' . $invoice->creditinvoice_parent_id, $invoice->creditinvoice_parent_id);
?>
                            <div class="col-xs-12">
                                <span class="label label-warning">
                                    <i class="fa fa-credit-invoice"></i>&nbsp;
                                    <?php echo trans('credit_invoice_for_invoice') . ' ' . $credit_link; ?>
                                </span>
                            </div>
<?php
}
?>

                            <div class="col-xs-12">

                                <div class="invoice-properties">
                                    <label><?php _trans('status');
                                    if ($invoice->is_read_only != 1 || $invoice->invoice_status_id != 4) {
                                        echo ' <span class="small">(' . trans('can_be_changed') . ')</span>';
                                    }
                                    ?>
                                    </label>
                                    <select name="invoice_status_id" id="invoice_status_id"
                                            class="form-control simple-select"
                                            <?php echo ($invoice->is_read_only == 1 && $invoice->invoice_status_id == 4) ? 'disabled="disabled"' : ''; ?>
                                    >
<?php
foreach ($invoice_statuses as $key => $status) {
?>
                                        <option value="<?php echo $key; ?>"
                                                <?php echo $key == $invoice->invoice_status_id ? 'selected="selected"' : ''; ?>
                                        >
                                            <?php echo $status['label']; ?>
                                        </option>
<?php
}
?>
                                    </select>
                                </div>

                                <div class="invoice-properties">
                                    <label><?php _trans('invoice'); ?> #</label>
                                    <input type="text" id="invoice_number"
                                           class="form-control"
                                        <?php if ($invoice->invoice_number) : ?>
                                            value="<?php echo $invoice->invoice_number; ?>"
                                        <?php else : ?>
                                            placeholder="<?php _trans('not_set'); ?>"
                                        <?php endif; ?>
                                        <?php echo $invoice->is_read_only ? 'disabled="disabled"' : ''; ?>
                                    >
                                </div>

                                <div class="invoice-properties has-feedback">
                                    <label><?php _trans('date'); ?></label>

                                    <div class="input-group">
                                        <input name="invoice_date_created" id="invoice_date_created"
                                               class="form-control datepicker"
                                               value="<?php echo date_from_mysql($invoice->invoice_date_created); ?>"
                                               <?php echo $invoice->is_read_only ? 'disabled="disabled"' : ''; ?>
                                        >
                                        <span class="input-group-addon">
                                        <i class="fa fa-calendar fa-fw"></i>
                                    </span>
                                    </div>
                                </div>

                                <div class="invoice-properties has-feedback">
                                    <label><?php _trans('due_date'); ?></label>

                                    <div class="input-group">
                                        <input name="invoice_date_due" id="invoice_date_due"
                                               class="form-control datepicker"
                                               value="<?php echo date_from_mysql($invoice->invoice_date_due); ?>"
                                               <?php echo $invoice->is_read_only ? 'disabled="disabled"' : ''; ?>
                                        >
                                        <span class="input-group-addon">
                                            <i class="fa fa-calendar fa-fw"></i>
                                        </span>
                                    </div>

                                </div>

                                <div class="invoice-properties">
                                    <label><?php _trans('payment_method'); ?></label>
                                    <select name="payment_method" id="payment_method"
                                            class="form-control simple-select"
                                            <?php echo ($invoice->is_read_only == 1 && $invoice->invoice_status_id == 4) ? 'disabled="disabled"' : ''; ?>
                                    >
                                        <option value="0"><?php _trans('select_payment_method'); ?></option>
<?php
foreach ($payment_methods as $payment_method) {
?>
                                        <option <?php check_select($invoice->payment_method, $payment_method->payment_method_id) ?>
                                            value="<?php echo $payment_method->payment_method_id; ?>">
                                            <?php echo $payment_method->payment_method_name; ?>
                                        </option>
<?php
} // End foreach
?>
                                    </select>
                                </div>

                                <div class="invoice-properties">
                                    <label><?php _trans('invoice_password'); ?></label>
                                    <input type="text" id="invoice_password" class="form-control"
                                           value="<?php _htmlsc($invoice->invoice_password); ?>"
                                           <?php echo $invoice->is_read_only ? 'disabled="disabled"' : ''; ?>>
                                </div>
                            </div>
<?php
$default_custom = false;
$classes        = ['control-label', 'controls', '', 'col-xs-12'];
foreach ($custom_fields as $custom_field) {
    if ( ! $default_custom && ! $custom_field->custom_field_location) {
        $default_custom = true;
    }

    if ($custom_field->custom_field_location == 1) {
        print_field($this->mdl_invoices, $custom_field, $custom_values, $classes[0], $classes[1], $classes[2], $classes[3]);
    }
}
?>

<?php
if ($invoice->invoice_status_id != 1) {
?>
                            <div class="col-xs-12">
                                <div class="form-group">
                                    <label for="invoice-guest-url"><?php _trans('guest_url'); ?></label>
                                    <div class="input-group">
                                        <input type="text" id="invoice-guest-url" readonly class="form-control"
                                               value="<?php echo site_url('guest/view/invoice/' . $invoice->invoice_url_key) ?>">
                                        <span class="input-group-addon to-clipboard cursor-pointer"
                                              data-clipboard-target="#invoice-guest-url">
                                            <i class="fa fa-clipboard fa-fw"></i>
                                        </span>
                                    </div>
                                </div>
                            </div>
<?php
} // End if
?>

                        </div>
                    </div>
                </div>

            </div>

<?php $this->layout->load_view('invoices/partial_itemlist_' . (get_setting('show_responsive_itemlist') ? 'responsive' : 'table')); ?>

            <hr/>

            <div class="row">
                <div class="col-xs-12 col-md-4">

                    <div class="panel panel-default no-margin">
                        <div class="panel-heading">
                            <?php _trans('sumex_observations'); ?>
                        </div>
                        <div class="panel-body">
                            <textarea id="invoice_sumex_observations" name="invoice_sumex_observations" class="form-control" rows="3"
                                      <?php echo $invoice->is_read_only ? 'disabled="disabled"' : ''; ?>
                            ><?php echo $invoice->sumex_observations; ?></textarea>
                        </div>
                    </div>

                </div>

                <div class="col-xs-12 col-md-4">

                    <div class="panel panel-default no-margin">
                        <div class="panel-heading">
                            <?php _trans('invoice_terms'); ?>
                        </div>
                        <div class="panel-body">
                            <textarea id="invoice_terms" name="invoice_terms" class="form-control" rows="3"
                                      <?php echo $invoice->is_read_only ? 'disabled="disabled"' : ''; ?>
                            ><?php _htmlsc($invoice->invoice_terms); ?></textarea>
                        </div>
                    </div>

                </div>

                <div class="col-xs-12 col-md-4">

                    <?php _dropzone_html($invoice->is_read_only); ?>

                </div>

                <div class="col-xs-12 visible-xs visible-sm"><br></div>

            </div>

<?php
if ($default_custom) {
?>
            <div class="row">
                <div class="col-xs-12">

                    <hr>

                    <div class="panel panel-default">
                        <div class="panel-heading"><?php _trans('custom_fields'); ?></div>
                        <div class="panel-body">
                            <div class="row">
<?php
    $classes = ['control-label', 'controls', '', 'form-group col-xs-12 col-sm-6'];
    foreach ($custom_fields as $custom_field) {
        if ( ! $custom_field->custom_field_location) { // == 0
            print_field($this->mdl_invoices, $custom_field, $custom_values, $classes[0], $classes[1], $classes[2], $classes[3]);
        }
    }
?>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
<?php
} // End if custom_fields
?>

        </div>
    </div>
</div>

<?php
_dropzone_script($invoice->invoice_url_key, $invoice->client_id);
