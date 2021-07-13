package net.redpwn.ctf;

import javax.swing.*;

public class JavaIsEZ3 {
    private static byte[] araragi = {
            0x3, 0x58, 0x48, 0x07, 0x53, // push 0x58480753
            0x3, 0x02, 0x46, 0x07, 0x46, // push 0x02460746
            0x3, 0x2B, 0x0A, 0x2E, 0x4C, // push 0x2B0A2E4C
            0x3, 0x2A, 0x00, 0x75, 0x05, // push 0x2A007505
            0x3, 0x09, 0x05, 0x71, 0x18, // push 0x09057118
            0x3, 0x36, 0x18, 0x0A, 0x1C, // push 0x36180A1C
            0x1, 0x0, // load register[0]
            0x4, // compare
            0x1, 0x1, // load register[1]
            0x4, // compare
            0x1, 0x2, // load register[2]
            0x4, // compare
            0x1, 0x3, // load register[3]
            0x4, // compare
            0x1, 0x4, // load register[4]
            0x4, // compare
            0x1, 0x5, // load register[5]
            0x4, // compare
            0x2  // kill vm
    };

    private static int[] hitagi = {
            /* 0 */ 0x1, 0x66, 0xD6, 0x39, 0x18, // push 0x66D63918
            /* 5 */ 0x0, 0x76, 0x70, 0x58, 0x76, 0x6B, 0x6E, 0x32, 0x2E, // push 0x767058766B6E322E
            /* 14 */ 0x0, 0x71, 0x43, 0x14, 0x6A, 0x70, 0x6E, 0x1F, 0x21, // push 0x7143146A706E1F21
            /* 23 */ 0x0, 0x6D, 0x66, 0x79, 0x43, 0x39, 0x4D, 0x39, 0x6D, // push 0x6D667943394D396D
            /* 32 */ 0x11, 0x4, // assign register[4]
            /* 34 */ 0x11, 0x5, // assign register[5]
            /* 36 */ 0x11, 0x6, // assign register[6]
            /* 38 */ 0x11, 0x7, // assign register[7]
            /* 40 */ 0x5, 47, // jmp 47
            /* 42 */ 0x3, 0x1, // push 0x1
            /* 44 */ 0x11, 0x0, // assign register[0]
            /* 46 */ 0x13, // kill vm
            /* 47 */ 0x4, 0x0, 0x4, // cmp r0, r4
            /* 50 */ 0x7, 42, // jnz 42
            /* 52 */ 0x4, 0x1, 0x5, // cmp r1, r5
            /* 55 */ 0x7, 42, // jnz 42
            /* 57 */ 0x4, 0x2, 0x6, // cmp r2, r6
            /* 60 */ 0x7, 42, // jnz 42
            /* 62 */ 0x4, 0x3, 0x7, // cmp r3, r7
            /* 65 */ 0x7, 42, // jnz 42
            /* 67 */ 0x13 // kill vm
    };

    private static boolean oshino(char[][] substrings) {
        // Check for "flag{d1d_y0u_kn0w?_chr1s"
        //int first =  0x36180A1C;
        //int second = 0x09057118;
        //int third =  0x2A007505;
        //int fourth = 0x2B0A2E4C;
        //int fifth =  0x02460746;
        //int sixth =  0x58480753;

        char[] bleh = substrings[1];
        if (new String(bleh).hashCode() != 998474623) {
            return false;
        }
        int[] registers = new int[6];
        int argsIndex = 0;
        for (int i = 0; i < hachikuji(bleh); i += 4) {
            registers[argsIndex++] = ((bleh[i] << 24)
                    | (bleh[i + 1] << 16)
                    | (bleh[i + 2] << 8)
                    | (bleh[i + 3])) ^ 0x07150715;
        }

        // VM
        int pc = 0;
        int[] stack = new int[0xf];
        int sp = 0;
        int result = 1;
        vm_loop:
        while (true) {
            int opcode = araragi[pc];

            switch (opcode) {
                case 0x0: { // assign register
                    int regIndex = araragi[pc + 1];
                    registers[regIndex] = stack[--sp];
                    pc += 2;
                    break;
                }
                case 0x1: { // load register
                    int regIndex = araragi[pc + 1];
                    stack[sp++] = registers[regIndex];
                    pc += 2;
                    break;
                }
                case 0x2: { // kill vm
                    break vm_loop;
                }
                case 0x3: { // load int
                    int theInt = (araragi[pc + 1] << 24)
                            | (araragi[pc + 2] << 16)
                            | (araragi[pc + 3] << 8)
                            | araragi[pc + 4];
                    stack[sp++] = theInt;
                    pc += 5;
                    break;
                }
                case 0x4: { // int compare
                    int op2 = stack[--sp];
                    int op1 = stack[--sp];
                    result &= (op1 == op2 ? 1 : 0);
                    pc += 1;
                    break;
                }
                case 0x5: { // load short
                    int theInt = (araragi[pc + 1] << 8)
                            | araragi[pc + 2];
                    stack[sp++] = theInt;
                    pc += 3;
                    break;
                }
                case 0x6: { // load byte
                    int theInt = araragi[pc + 1];
                    stack[sp++] = theInt;
                    pc += 2;
                    break;
                }
            }
        }

        return result == 1;
    }

    private static boolean sengoku(char[][] substrings) {
        // _is_4_Hu_Tao_s1mp!_0715}
        // 0 = 0x6D667943394D396D
        // 1 = 0x7143146A706E1F21
        // 2 = 0x767058766B6E322E
        // 3 = 0x66D63918
        char[] bleh = substrings[2];
        long[] registers = new long[0xf];
        int argsIndex = 0;
        for (int i = 0; i < hachikuji(bleh); i += 8) {
            registers[argsIndex++] = (
                    ((long) bleh[i] << 56)
                            | ((long) bleh[i + 1] << 48)
                            | ((long) bleh[i + 2] << 40)
                            | ((long) bleh[i + 3] << 32)
                            | ((long) bleh[i + 4] << 24)
                            | ((long) bleh[i + 5] << 16)
                            | ((long) bleh[i + 6] << 8)
                            | bleh[i + 7]
            ) ^ 0x0302071503020715L;
        }
        registers[argsIndex] = new String(bleh).hashCode();

        // VM
        int pc = 0;
        long[] stack = new long[0xf];
        int sp = 0;
        vm_loop:
        while (true) {
            int opcode = hitagi[pc];

            switch (opcode) {
                case 0x0: { // load long
                    long theLong = (((long) hitagi[pc + 1] << 56)
                            | ((long) hitagi[pc + 2] << 48)
                            | ((long) hitagi[pc + 3] << 40)
                            | ((long) hitagi[pc + 4] << 32)
                            | ((long) hitagi[pc + 5] << 24)
                            | ((long) hitagi[pc + 6] << 16)
                            | ((long) hitagi[pc + 7] << 8)
                            | hitagi[pc + 8]);
                    stack[sp++] = theLong;
                    pc += 9;
                    break;
                }
                case 0x1: { // load int
                    long theLong = (((long) hitagi[pc + 1] << 24)
                            | ((long) hitagi[pc + 2] << 16)
                            | ((long) hitagi[pc + 3] << 8)
                            | hitagi[pc + 4]);
                    stack[sp++] = theLong;
                    pc += 5;
                    break;
                }
                case 0x2: { // load short
                    long theLong = (((long) hitagi[pc + 1] << 8)
                            | hitagi[pc + 2]);
                    stack[sp++] = theLong;
                    pc += 3;
                    break;
                }
                case 0x3: { // load byte
                    long theLong = hitagi[pc + 1];
                    stack[sp++] = theLong;
                    pc += 2;
                    break;
                }
                case 0x4: { // cmp
                    int leftIndex = hitagi[pc + 1];
                    int rightIndex = hitagi[pc + 2];
                    registers[0] = registers[leftIndex] == registers[rightIndex] ? 0 : 1;
                    pc += 3;
                    break;
                }
                case 0x5: { // jmp
                    pc = hitagi[pc + 1];
                    break;
                }
                case 0x6: { // jz
                    if (registers[0] == 0) {
                        pc = hitagi[pc + 1];
                    } else {
                        pc += 2;
                    }
                    break;
                }
                case 0x7: { // jnz
                    if (registers[0] != 0) {
                        pc = hitagi[pc + 1];
                    } else {
                        pc += 2;
                    }
                    break;
                }
                case 0x8: { // xor
                    int leftIndex = hitagi[pc + 1];
                    int rightIndex = hitagi[pc + 2];
                    registers[leftIndex] = registers[leftIndex] ^ registers[rightIndex];
                    pc += 3;
                    break;
                }
                case 0x9: { // or
                    int leftIndex = hitagi[pc + 1];
                    int rightIndex = hitagi[pc + 2];
                    registers[leftIndex] = registers[leftIndex] | registers[rightIndex];
                    pc += 3;
                    break;
                }
                case 0x10: { // and
                    int leftIndex = hitagi[pc + 1];
                    int rightIndex = hitagi[pc + 2];
                    registers[leftIndex] = registers[leftIndex] & registers[rightIndex];
                    pc += 3;
                    break;
                }
                case 0x11: { // assign register
                    int regIndex = hitagi[pc + 1];
                    registers[regIndex] = stack[--sp];
                    pc += 2;
                    break;
                }
                case 0x12: { // load register
                    int regIndex = hitagi[pc + 1];
                    stack[sp++] = registers[regIndex];
                    pc += 2;
                    break;
                }
                case 0x13: { // kill vm
                    break vm_loop;
                }
            }
        }

        return registers[0] == 0;
    }

    private static void kanbaru(char[][] substrings) {
        for (int i = 0; i < hachikuji(substrings) - 1; i++) {
            char[] first = substrings[i];
            char[] second = substrings[i + 1];
            for (int j = 0; j < hachikuji(first); j++) {
                second[j] ^= first[j];
            }
        }
    }

    public static int hachikuji(Object o) {
        try {
            var clazz = Class.forName("java.lang.reflect.Array");
            var method = clazz.getDeclaredMethod("getLength", Object.class);
            method.setAccessible(true);
            return (int) method.invoke(null, o);
        } catch (Throwable t) {
            throw new RuntimeException("Ayaya!");
        }
    }

    public static void main(String[] args) {
        //args = new String[]{"flag{d1d_y0u_kn0w?_chr1s_is_4_Hu_Tao_s1mp!_0715}"};
        if (hachikuji(args) == 0) {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                JOptionPane.showMessageDialog(null, "Silly-churl, billy-churl, silly-billy hilichurl... Woooh!\n~A certain Wangsheng Funeral Parlor director\n\n(This is not the flag, btw)");
            } catch (Throwable ignore) {
            }
        } else {
            if (args[0].length() != 48) {
                System.out.println("*fanfare* You've been pranked!");
                return;
            }
            char[] iv = "WalnutGirlBestGirl_07/15".toCharArray();
            char[][] substrings = new char[3][];
            substrings[0] = iv;
            int subLen = args[0].length() / 2;
            for (int i = 0; i < 2; i++) {
                substrings[i + 1] = args[0].substring(i * subLen, (i + 1) * subLen).toCharArray();
            }
            kanbaru(substrings);
            if (oshino(substrings) & sengoku(substrings) & (args[0].hashCode() == 1101317042)) {
                System.out.println("Chute.  Now you know my secret");
            } else {
                System.out.println("*fanfare* You've been pranked!");
            }
        }
    }
}
