$fn = 50;
radius = 0.625;
extent_height = 1.600;
chamfer_height = 0.150;
chamfer_inset = 0.300;

screw_hole_z_offset = 0.431;
screw_hole_r = 0.199;

collar_void = 0.56;
collar_radius = 0.5234;

glue_channel_pattern_radius = radius - 0.2;
glue_channel_radius = 0.0825;
glue_channel_n = 5;
        
difference() {
    union() {
        translate([0,0,chamfer_height])
            cylinder(h=extent_height-chamfer_height,r=radius);
        cylinder(chamfer_height, r1 = radius-chamfer_inset, r2 = radius);
    }


    union() {
        translate([0,0,0.47])
            cylinder(h = collar_void, r=collar_radius, $fn = 50, center = true); 
        
        
        cylinder(h = 0.5, r = .255, $fn = 35, center = true);
        
        translate([radius,0,screw_hole_z_offset])
            rotate([0,90,0])
                cylinder(h=0.5,r=screw_hole_r,center = true,$fn=25);

        difference() {
            translate([0,0,0.18])
                cylinder(h = 0.05, r = .7, center = true);
            translate([0,0,0.18])
                cylinder(h = 0.5, r = 0.60, center = true);
        }
        
        step = 360/glue_channel_n;
        for (i = [0:glue_channel_n-1]) {
          angle = i * step;
          dx = glue_channel_pattern_radius * cos(angle);
          dy = glue_channel_pattern_radius * sin(angle);
          translate([dx, dy, 0.881]) cylinder(extent_height, r=glue_channel_radius, $fn=10);
        }
        
        translate([0, 0, 0.881]) cylinder(extent_height, r=glue_channel_radius, $fn=10);
        
    }
}

