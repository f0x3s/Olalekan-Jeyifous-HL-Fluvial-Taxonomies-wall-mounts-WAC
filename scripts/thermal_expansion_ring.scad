union() {
    translate([0,0,0.48])
        cylinder(h = 0.56, r=0.51, $fn = 100, center = true); 

    difference() {
        translate([0,0,0.18])
            cylinder(h = 0.05, r = .7, center = true, $fn = 100);
        translate([0,0,0.18])
            cylinder(h = 0.5, r = 0.60, center = true, $fn = 100);
    }
}
