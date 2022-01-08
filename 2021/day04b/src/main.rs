use std::fs::File;
use std::io::{BufRead, BufReader, Result};

fn transpose<T>(v: Vec<Vec<T>>) -> Vec<Vec<T>> {
    assert!(!v.is_empty());
    let len = v[0].len();
    let mut iters: Vec<_> = v.into_iter().map(|n| n.into_iter()).collect();
    (0..len)
        .map(|_| {
            iters
                .iter_mut()
                .map(|n| n.next().unwrap())
                .collect::<Vec<T>>()
        })
        .collect()
}

fn check_win_condition_rows(marked: Vec<Vec<bool>>) -> bool {
    marked.iter().fold(false, |row_acc, row| {
        row.iter().fold(true, |el_acc, el| *el && el_acc) || row_acc
    })
}

fn check_win_condition(marked: &Vec<Vec<bool>>) -> bool {
    check_win_condition_rows(marked.clone()) || check_win_condition_rows(transpose(marked.clone()))
}

fn compute_score(board: &Vec<Vec<usize>>, marked: &Vec<Vec<bool>>, last_input: usize) -> usize {
    board
        .into_iter()
        .enumerate()
        .map(|(i, row)| {
            row.into_iter()
                .enumerate()
                .map(|(j, el)| if marked[i][j] { 0 } else { *el })
                .sum::<usize>()
        })
        .sum::<usize>()
        * last_input
}

fn simulate_for_board(board: &Vec<Vec<usize>>, inputs: &Vec<usize>) -> Option<(usize, Vec<Vec<bool>>)> {
    assert!(!board.is_empty());
    let mut marked = vec![vec![false; board[0].len()]; board.len()];
    for (turn, input) in inputs.iter().enumerate() {
        if let Some((i, j)) = board.iter().enumerate().fold(None, |acc, (i, row)| {
            if let Some(j) = row.iter().position(|el| el == input) {
                Some((i, j))
            } else {
                acc
            }
        }) {
            marked[i][j] = true;
            if check_win_condition(&marked) {
                return Some(((turn) as usize, marked));
            }
        }
    }
    None
}

fn main() -> Result<()> {
    let input_file = File::open("data/input.txt")?;
    let mut lines = BufReader::new(input_file).lines();

    let inputs: Vec<usize> = lines
        .next()
        .unwrap()
        .unwrap()
        .split(",")
        .map(|el| el.parse::<usize>().unwrap())
        .collect();

    let mut res: Option<(Vec<Vec<usize>>, Vec<Vec<bool>>)> = None; // (turn, board, marked)
    let mut res_turn = 0;

    let mut buf: Vec<Vec<usize>> = Vec::new();
    for line in lines {
        if let Ok(l) = line {
            if !l.is_empty() {
                buf.push(l
                    .split(" ")
                    .filter(|&el| !el.is_empty())
                    .map(|el| el.parse::<usize>().unwrap()
                ).collect());
                continue;
            }
            if !buf.is_empty() {
                if let Some((turn, marked)) = simulate_for_board(&buf, &inputs) {
                    if turn > res_turn {
                        res = Some((buf.clone(), marked.clone()));
                        res_turn = turn;
                    }
                }
                buf = Vec::new();
            }
        }
    }

    if let Some((board, marked)) = res {
        println!("The final score was: {}", compute_score(&board, &marked, inputs[res_turn]));
    } else {
        println!("There was no winners");
    }

    Ok(())
}
