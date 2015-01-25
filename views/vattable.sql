DROP VIEW IF EXISTS vr_vattable;

CREATE VIEW
  vr_vattable
AS SELECT DISTINCT
  vr_vatrates.country,
  vr_vatrates.code,
  standard.rate_value as standard,
  coalesce(reduced1.rate_value,'') as reduced_1,
  coalesce(reduced2.rate_value,'') as reduced_2,
  coalesce(super_reduced.rate_value,'') as super_reduced,
  coalesce(parking.rate_value,'') as parking
FROM
  vr_vatrates,
  vr_vatrates as standard,
  vr_vatrates as reduced1,
  vr_vatrates as reduced2,
  vr_vatrates as super_reduced,
  vr_vatrates as parking
WHERE
  vr_vatrates.code = standard.code AND
  vr_vatrates.code = reduced1.code AND
  vr_vatrates.code = reduced2.code AND
  vr_vatrates.code = super_reduced.code AND
  vr_vatrates.code = parking.code AND
  standard.rate_name = "standard" AND
  parking.rate_name = "parking" AND
  super_reduced.rate_name = "super_reduced" AND
  reduced1.rate_name = "reduced_1" AND
  reduced2.rate_name = "reduced_2" 
ORDER BY 
  vr_vatrates.eusort;

