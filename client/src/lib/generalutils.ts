export function chars(): string {
    let chars = "";
    for (let i = 32; i < 127; i++) {
        chars += String.fromCharCode(i);
    }
    return chars;
}

export function randomString(length: number) {
    let result = '';
    let characters = chars(); // All ASCII characters
    let charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

// export function check(x: any): boolean {
//     if (x == null) {
//         return false;
//     }

//     if (x === null) {
//         return false;
//     }

//     if (typeof x === 'undefined') {
//         return false;
//     }

//     return true;
// }