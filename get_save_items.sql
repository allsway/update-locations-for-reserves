SELECT barcode,'OITYPE=' || save_itype_code_num || ', ' || 'OLOCAT=' || rpad(save_location_code,5) || ', ' || 'OCHKOUT=' || save_checkout_total AS "Save item"
FROM sierra_view.item_view
WHERE save_location_code IS NOT NULL;
