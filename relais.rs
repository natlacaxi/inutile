use std::io;
fn main() {
    let mut l = String::new();
    io::stdin().read_line(&mut l).unwrap();
    let (v, t) = l.trim_end().split_once('\t').unwrap();
    println!("{}\t{}>Rust", v, t);
}
