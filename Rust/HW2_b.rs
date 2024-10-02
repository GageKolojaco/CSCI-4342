use std::env;
use std::fs::File;
use std::io;
use std::io::BufRead;

fn main() {
    if let Some(filename) = env::args().nth(1) { 
        match File::open(&filename) { 
            Ok(file) => { 
                let diagnostics = load_diagnostics(io::BufReader::new(file)); 
                let life_support = check_life_support(diagnostics); 
                println!("Life Support rate: {}", life_support); 
            }
            Err(error) => eprintln!("Cannot open file: {}", error) 
        }
    }
    else{ 
        eprintln!("Can't execute program, please run like this and make sure the file is in the same folder: csci4342_HW2.rs <filename>.txt")
    }
}

fn load_diagnostics<E: BufRead>(reader: E) -> Vec<Vec<char>> {
    println!("Loading diagnostics...");
    let mut binary_strings = Vec::new(); 
    for line in reader.lines() { 
        if let Ok(line) = line { 
            let line = line.trim().to_string(); 
            if !line.is_empty() { 
                binary_strings.push(line); 
            }
        }
    }
    let max_length = binary_strings[0].len(); 
    let mut vec_of_binary_str: Vec<Vec<char>> = vec![Vec::new(); max_length]; 
    for str in binary_strings { 
        for (index, char) in str.chars().enumerate() { 
            vec_of_binary_str[index].push(char); 
        }
    }
    return vec_of_binary_str
}

fn check_life_support (vec_of_binary_str: Vec<Vec<char>>) -> i32 { 
    let mut o2_scrubber = String::new();
    let mut co2_scrubber = String::new();
    let mut remaining_o2 = vec_of_binary_str.clone();
    let mut remaining_co2 = vec_of_binary_str.clone();
    
    for i in 0..vec_of_binary_str.len() {
        if remaining_o2.len() > 1 {
            let count_0 = remaining_o2[i].iter().filter(|&&c| c == '0').count();
            let count_1 = remaining_o2[i].iter().filter(|&&c| c == '1').count();
            let most_common = if count_0 > count_1 { '0' } else { '1' };
            remaining_o2.retain(|x| x[i] == most_common);
        }
        
        if remaining_co2.len() > 1 {
            let count_0 = remaining_co2[i].iter().filter(|&&c| c == '0').count();
            let count_1 = remaining_co2[i].iter().filter(|&&c| c == '1').count();
            let least_common = if count_0 <= count_1 { '0' } else { '1' };
            remaining_co2.retain(|x| x[i] == least_common);
        }
    }
    
    for i in 0..vec_of_binary_str.len() {
        o2_scrubber.push(remaining_o2[0][i]);
        co2_scrubber.push(remaining_co2[0][i]);
    }
    
    println!("O2 Generator computed...");
    println!("CO2 Scrubber rate computed...");
    let o2_scrubber_int = i32::from_str_radix(&o2_scrubber, 2).unwrap(); 
    let co2_scrubber_int = i32::from_str_radix(&co2_scrubber, 2).unwrap();// 
    return o2_scrubber_int * co2_scrubber_int
}