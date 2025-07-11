<div class="row">
    <div class="col-xs-12 col-md-8 col-md-offset-2">

        <div class="panel panel-default">
            <div class="panel-heading">
                <?php _trans('taxes'); ?>
            </div>
            <div class="panel-body">

                <div class="row">
                    <div class="col-xs-12 col-md-6">

                        <div class="form-group">
                            <label for="settings[default_invoice_tax_rate]">
                                <?php _trans('default_invoice_tax_rate'); ?>
                            </label>
                            <select name="settings[default_invoice_tax_rate]" id="settings[default_invoice_tax_rate]"
                                class="form-control simple-select">
                                <option value=""><?php _trans('none'); ?></option>
<?php foreach ($tax_rates as $tax_rate) { ?>
                                <option value="<?php echo $tax_rate->tax_rate_id; ?>"
                                    <?php check_select(get_setting('default_invoice_tax_rate'), $tax_rate->tax_rate_id); ?>>
                                    <?php echo $tax_rate->tax_rate_percent . '% - ' . $tax_rate->tax_rate_name; ?>
                                </option>
<?php } ?>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="settings[default_item_tax_rate]">
                                <?php _trans('default_item_tax_rate'); ?>
                            </label>
                            <select name="settings[default_item_tax_rate]" id="settings[default_item_tax_rate]"
                                class="form-control simple-select">
                                <option value=""><?php _trans('none'); ?></option>
<?php foreach ($tax_rates as $tax_rate) { ?>
                                <option value="<?php echo $tax_rate->tax_rate_id; ?>"
                                    <?php check_select(get_setting('default_item_tax_rate'), $tax_rate->tax_rate_id); ?>>
                                    <?php echo $tax_rate->tax_rate_percent . '% - ' . $tax_rate->tax_rate_name; ?>
                                </option>
<?php } ?>
                            </select>
                        </div>

                    </div>

<?php
// LEGACY_CALCULATION false : Taxes Global N, Item Y : Use simple calculation : Apply global discount before item tax
// For e-invoices : 🗸 EN16931, ? PEPPOL3BIS, ? UBL, ? CII ••• (WIP : todo: checks, modify, create models).
if ( ! $legacy_calculation) {
?>
                    <input name="settings[default_include_item_tax]" id="settings[default_include_item_tax]" type="hidden" value="">
<?php
}
// LEGACY_CALCULATION true : Taxes Global Y, Item Y : Use legacy calculation for Discounts & Taxes : By default in ipconfig.
else {
?>
                    <div class="col-xs-12 col-md-6">
                        <div class="form-group">
                            <label for="settings[default_include_item_tax]">
                                <?php _trans('default_invoice_tax_rate_placement'); ?>
                            </label>
                            <select name="settings[default_include_item_tax]" id="settings[default_include_item_tax]"
                                class="form-control simple-select" data-minimum-results-for-search="Infinity">
                                <option value=""><?php _trans('none'); ?></option>
                                <option value="0" <?php check_select(get_setting('default_include_item_tax'), '0'); ?>>
                                    <?php _trans('apply_before_item_tax'); ?>
                                </option>
                                <option value="1" <?php check_select(get_setting('default_include_item_tax'), '1'); ?>>
                                    <?php _trans('apply_after_item_tax'); ?>
                                </option>
                            </select>
                        </div>
                    </div>
<?php
} // Fi LEGACY_CALCULATION (Show or not Global Taxes) - since v1.6.3
?>
                </div>

            </div>
        </div>

    </div>
</div>
