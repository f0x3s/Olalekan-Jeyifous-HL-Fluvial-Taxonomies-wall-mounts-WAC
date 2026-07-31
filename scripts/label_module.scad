union() {
    // label
    translate([text_x, text_y, layer_height/2])
        linear_extrude(height = text_height)
            text(
                label_text,
                size = text_size,
                halign = "center",
                valign = "center"
            );
    
    // brim
    difference() {
        translate([0, -0.25, 1 * layer_height/2])
            cube([2.125, 1.5, layer_height], center = true);
        translate([0, 0, layer_height])
            cylinder(h = layer_height, r = 0.34, $fn = 100, center = true);
    }
}