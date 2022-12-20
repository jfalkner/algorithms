BWT Implemenation in Rust
---

An implementation of [BWT](https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform) in Rust. This algorithm is an easy fizz-buzz like example often asked in computational biology interviews. The code includes several `println!` statements to show state at various points in the algorithm. The intention here is not to make an API nor do a performance test. This work was done while learning Rust and starting to compare it to Python.

Compile the code with `rustc`.
```
rustc bwt.rs
```

Use `stdin` to send a string to the code and it'll return the BWT of the string. In the below example, "apple" is used and the expected result is "elppa".
```
$ echo "apple" | ./bwt
String to transform: apple

Rotated:
apple
pplea
pleap
leapp
eappl

Sorted:
apple
eappl
leapp
pleap
pplea

Final BWT
elppa
```
