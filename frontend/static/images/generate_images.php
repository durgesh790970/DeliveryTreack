<?php
// Simple PHP script to generate placeholder food images
// Run this once to generate all food category images

$categories = [
    'pizza' => ['#FF6B35', '🍕'],
    'burger' => ['#F7931E', '🍔'],
    'biryani' => ['#8B4513', '🍛'],
    'chicken' => ['#D4A574', '🍗'],
    'dosa' => ['#DAA520', '🥘'],
    'noodles' => ['#FFD700', '🍜'],
    'dessert' => ['#FF69B4', '🍰'],
    'beverage' => ['#4169E1', '🥤'],
    'paneer' => ['#FFE4B5', '🧀'],
    'sushi' => ['#FF4500', '🍣'],
];

$imageDir = __DIR__ . '/images/';
if (!is_dir($imageDir)) {
    mkdir($imageDir, 0755, true);
}

foreach ($categories as $name => $data) {
    createCategoryImage($imageDir, $name, $data[0], $data[1]);
}

function createCategoryImage($dir, $name, $color, $emoji) {
    $filename = $dir . $name . '.jpg';
    
    // Create a 400x300 image with gradient and emoji
    $img = imagecreatetruecolor(400, 300);
    
    // Parse hex color
    $rgb = hex2rgb($color);
    $bgColor = imagecolorallocate($img, $rgb[0], $rgb[1], $rgb[2]);
    $darkColor = imagecolorallocate($img, max(0, $rgb[0]-30), max(0, $rgb[1]-30), max(0, $rgb[2]-30));
    $whiteColor = imagecolorallocate($img, 255, 255, 255);
    
    // Fill gradient
    for ($y = 0; $y < 300; $y++) {
        $ratio = $y / 300;
        $r = intval($rgb[0] * (1 - $ratio * 0.3));
        $g = intval($rgb[1] * (1 - $ratio * 0.3));
        $b = intval($rgb[2] * (1 - $ratio * 0.3));
        $color = imagecolorallocate($img, $r, $g, $b);
        imageline($img, 0, $y, 400, $y, $color);
    }
    
    // Add text
    $fontPath = __DIR__ . '/fonts/arial.ttf';
    $text = ucfirst($name);
    
    // Add emoji-like text in center
    imagestring($img, 5, 150, 100, $emoji . ' ' . $emoji, $whiteColor);
    imagestring($img, 3, 120, 180, $text, $whiteColor);
    
    imagejpeg($img, $filename, 85);
    imagedestroy($img);
    
    echo "Created: $filename\n";
}

function hex2rgb($hex) {
    $hex = ltrim($hex, '#');
    $data = array_map('hexdec', str_split($hex, 2));
    return array_pad($data, 3, 0);
}

echo "Image generation complete!\n";
?>
