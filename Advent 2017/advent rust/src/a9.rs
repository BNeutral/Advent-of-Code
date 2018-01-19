#[allow(dead_code)]
pub fn advent9_1(input : &str) -> u32 {
    find_score(input, false)
}

#[allow(dead_code)]
pub fn advent9_2(input : &str) -> u32 {
    find_score(input, true)
}

/// Finds the score of the problem according to the rules for counting group scores
/// If second part is passed, instead it counts the characters in the garbage
/// Assumes proper input and panics if there is any unmatched closing "}"
fn find_score(input : &str, second_part : bool) -> u32 {
    let mut parsing_trash : bool = false;
    let mut canceled : bool = false;
    let mut bracket_depth : u32 = 0;
    let mut result : u32 = 0;
    for char in input.chars() {
        if canceled {
            canceled = false;
            continue;
        }
        if parsing_trash {
            match char {
                '>' => parsing_trash = false,
                '!' => canceled = true,
                _ => { if second_part { result += 1 } }
            }
            continue;
        }
        match char {
            '{' => bracket_depth += 1,
            '}' => {
                if !second_part { result += bracket_depth; }
                bracket_depth -= 1;

            },
            '<' => parsing_trash = true,
            _ => {},
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        let str = "{}";
        assert_eq!(1,advent9_1(str));
    }

    #[test]
    fn test1_2() {
        let str = "{{{}}}";
        assert_eq!(6,advent9_1(str));
    }

    #[test]
    fn test1_3() {
        let str = "{{},{}}";
        assert_eq!(5,advent9_1(str));
    }

    #[test]
    fn test1_4() {
        let str = "{{{},{},{{}}}}";
        assert_eq!(16,advent9_1(str));
    }

    #[test]
    fn test1_5() {
        let str = "{<a>,<a>,<a>,<a>}";
        assert_eq!(1,advent9_1(str));
    }

    #[test]
    fn test1_6() {
        let str = "{{<ab>},{<ab>},{<ab>},{<ab>}}";
        assert_eq!(9,advent9_1(str));
    }

    #[test]
    fn test1_7() {
        let str = "{{<!!>},{<!!>},{<!!>},{<!!>}}";
        assert_eq!(9,advent9_1(str));
    }

    #[test]
    fn test1_8() {
        let str = "{{<a!>},{<a!>},{<a!>},{<ab>}}";
        assert_eq!(3,advent9_1(str));
    }

    #[test]
    fn test2_1() {
        let str = "<>";
        assert_eq!(0,advent9_2(str));
    }


    #[test]
    fn test2_2() {
        let str = "<random characters>";
        assert_eq!(17,advent9_2(str));
    }

    #[test]
    fn test2_3() {
        let str = "<<<<>";
        assert_eq!(3,advent9_2(str));
    }

    #[test]
    fn test2_4() {
        let str = "<{!>}>";
        assert_eq!(2,advent9_2(str));
    }

    #[test]
    fn test2_5() {
        let str = "<!!>";
        assert_eq!(0,advent9_2(str));
    }

    #[test]
    fn test2_6() {
        let str = "<!!!>>";
        assert_eq!(0,advent9_2(str));
    }

    #[test]
    fn test2_7() {
        let str = "<{o\"i!a,<{i<a>";
        assert_eq!(10,advent9_2(str));
    }

}
