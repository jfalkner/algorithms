use std::io::{self, BufRead};

fn main() {
    // Read a line of text from stdin
    let mut line = String::new();
    let stdin = io::stdin();
    stdin.lock().read_line(&mut line).unwrap();
    let text = line.trim_end();
    println!("String to transform: {}", text);

    // Calcuate all the rotations
    println!("\nRotated:");
    let mut vec: Vec<String> = Vec::new();
    let l = text.len();
    for n in 0..l{
        let a = &text[0..n];
        let b = &text[n..l];
        let rotated = [b, a].concat();
        println!("{}", rotated);
        vec.push(rotated);
    }

    // Display the sorted strings
    println!("\nSorted:");
    vec.sort();
    for v in vec.iter() {
        println!("{}", v);
    }

    // Calculate the final BWT
    println!("\nFinal BWT");
    let mut bwt: Vec<char> = Vec::new();
    for v in vec.iter() {
        bwt.push(v.chars().last().unwrap());
    }
    println!("{}", bwt.into_iter().collect::<String>());
}
