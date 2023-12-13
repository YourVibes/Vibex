# Vibex | Programming Language
A programming language for writing code the way you want it.<br>
Written in <strong>Python</strong> and translated into <strong>C++</strong>.<br>
<img alt="Logo" src="./logo/logo.png"><br>
Made with 💜 by <strong>YourVibes™</strong>.<br>
Main developer: <strong>Christian Alessandri</strong>.<br>
Secondary developer: <strong>Davide Sciaulino</strong>.<br><br>
<i>⚠️ For proper operation, the transcompiler requires you to have installed on your development environment: <strong>python3</strong> and <strong>gcc compiler</strong>.</i>
  
  
## Transcompiler commands
Compile .vbx into **executable file**.
```shell
python3 vibex.py -c file.vbx
```
  
Get the **C++ file** of .vbx source code.
```shell
python3 vibex.py -s file.vbx
# or
python3 vibex.py -s --cpp file.vbx
```
  
Get the **assembly file** of .vbx source code.
```shell
python3 vibex.py -s --asm file.vbx
```
  
Get the compiler version.
```shell
python3 vibex.py -v
# or
python3 vibex.py --version
```
  
Get help
```shell
python3 vibex.py -h
# or
python3 vibex.py --help
```
  
## Grammar 🖋️  
  
### 🧮 Basic Operations 🧮
**Arithmetic**
| Operator    | Name           | Description                                        |
|-------------|----------------|----------------------------------------------------|
| +           | Addition       | Adds together two values                           |
| -           | Subtraction    | Subtracts one value from another                   |
| *           | Multiplication | Multiplies two values                              |
| /           | Division       | Divides one value by another                       |
| %           | Modulus        | Returns the division remainder                     |
| **          | Power          | Returns the value of base to the power of exponent |
| (\| ... \|) | Absolute value | Returns the absolute value of an expression        |
  
**Bitwise**
| Operator | Name        |
|----------|-------------|
| &        | AND         |
| \|       | OR          |
| ^        | XOR         |
| <<       | Left shift  |
| >>       | Right shift |
| ~        | NOT         |
  
**Assignment**
| Operator | Name                      | Description                                                                                                                                                                                |
|----------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| =        | Assignment                | Assigns the value on the right to the variable on the left                                                                                                                                 |
| +=       | Addition assignment       | Adds the current value of the variable on the left to the value on the right and then assigns the result to the variable on the left                                                       |
| -=       | Subtraction assignment    | Subtracts the value on the right from the current value of the variable on the left and then assigns the result to the variable on the left                                                |
| *=       | Multiplication assignment | Multiplies the current value of the variable on the left by the value on the right and then assigns the result to the variable on the left                                                 |
| /=       | Division assignment       | Divides the current value of the variable on the left by the value on the right and then assigns the result to the variable on the left                                                    |
| %=       | Modulus assignment        | Computes the modulus of the current value of the variable on the left divided by the value on the right and assigns the result to the variable on the left                                 |
| &=       | Bitwise AND assignment    | Performs a bitwise AND between the current value of the variable on the left and the value on the right, then assigns the result to the variable on the left                               |
| \|=      | Bitwise OR assignment     | Performs a bitwise OR between the current value of the variable on the left and the value on the right, then assigns the result to the variable on the left                                |
| ^=       | Bitwise XOR assignment    | Performs a bitwise XOR between the current value of the variable on the left and the value on the right, then assigns the result to the variable on the left                               |
| <<=      | Left Shift assignment     | Left shifts the bits of the current value of the variable on the left by the number of positions specified by the value on the right, then assigns the result to the variable on the left  |
| >>=      | Right Shift assignment    | Right shifts the bits of the current value of the variable on the left by the number of positions specified by the value on the right, then assigns the result to the variable on the left |

  
**Comparison**
| Operator | Name                     |
|----------|--------------------------|
| ==       | Equal to	              |
| !=       | Not equal	              |
| >        | Greater than	          |
| <        | Less than	              |
| >=       | Greater than or equal to |
| <=       | Less than or equal to	  |
  
**Logical**
| Operator | Name        |
|----------|-------------|
| &&       | Logical AND |
| \|\|     | Logical OR	 |
| !        | Logical NOT |
  
#### For example
**Power**
```java
var:double foo = 2**4
print foo                   # expected output: 16
```
  
**Absolute value**
```java
var:int foo = (| 4-6 |)     # foo = |-2| = 2
var:int bar = (| foo-12 |)  # bar = |-10| = 10
print bar                   # expected output: 10
```
  
  
### 📦 Variables 📦  
**Types**  
| Name               | Type     | Notes                  |
|--------------------|----------|------------------------|
| short int          | s_int    |                        |
| int                | int      |                        |
| long int           | l_int    |                        |
| float              | float    |                        |
| double             | double   |                        |
| long double        | l_double |                        |
| char               | char     |                        |
| unsigned short int | us_int   |                        |
| unsigned int       | u_int    |                        |
| unsigned long int  | ul_int   |                        |
| unsigned char      | u_char   |                        |
| boolean            | bool     |                        |
| string             | string   |                        |
| wide string        | wstring  |                        |
| void               | void     | Only for the functions |

  
**Declaration**  
```java
var:type name;
```
  
**Initialisation**  
```java
var:type name = value;
```
  
**Usage**  
```java
name = value;
```
  
**Strings**  
You can write text strings either by wrapping them between " or '  
```java
var:string name = "Hello, world!";
var:string name = 'Hello, world!';
```
  
**Binary, Octal, Decimal & Hexadecimal**
```java
# Binary
name = bin value;

# Octal
name = oct value;

# Decimal
name = dec value; # If you do not specify the numbering system the default is decimal

# Hexadecimal
name = hex value;
```
  
*It is also possible to write all instructions without a semicolon, but in this case a carriage return is required*
  
  
### 🔢 Arrays 🔢
**Declaration**  
```java
arr[dim]:type name;
```
  
**Initialization**  
```java
arr[dim]:type name = {a, b, c};
```
  
**Usage**  
```java
name[i] = value;
```
  
*It is also possible to write all instructions without a semicolon, but in this case a carriage return is required*
  
  
### 🌐 Global 🌐  
```java
# You can create a global variable
global var:type name;
# or a global array
global arr[dim]:type name;
```
  
  
### ⌨️ I/O 🖥️  
**Input**  
```java
input(foo);
# or
in(foo);
```
You can also write them without parentheses or semicolon.
```java
# It is right ✅
input|in foo;
  
# It is also right ✅
input|in foo
```
  
**Output**  
```java
# If it is a variable...
print(foo);
  
# If it is a string...
print("Hello, World!");
```
You can also write them without parentheses or semicolon.
```java
# It is right ✅
print foo;
  
# It is also right ✅
print "Hello, World!"
```
To go to the next line you can use the println.
```java
println("Hello, World!");
```
  
If you want to print unicode characters, you can use wprint or wprintln.
```java
var:wstring emoji = "\U0001F604";
wprint(emoji);
# Expected output: 😄
```
And if you don't feel like looking up unicodes, you can do this....
```java
var:wstring emoji = "😄";
wprint(emoji);
```
  
  
### 🧐 Conditions 🧐  
**If, Else if & Else**
```java
if (condition) {
    ...
} elif (condition) {
    ...
} else condition {
    ...
}
```
You can also write conditions without parentheses and, in addition, you can write *else if* instead of *elif*.
```java
if condition {
    ...
} else if condition {
    ...
} else condition {
    ...
}
```
  
**Switch-Case**
```java
switch(value) {
    case value:
        break;
    case value:
        break;
    ...
    default:
        break;
}
```
You can also write the condition without parentheses.
```java
switch value {
    ...
}
```
  
#### Logical Operators
**And**  
```java
if expr && expr {
    ...
}
# or
if expr and expr {
    ...
}
```
  
**Or**  
```java
if expr || expr {
    ...
}
# or
if expr or expr {
    ...
}
```
  
**Not**  
```java
if !expr {
    ...
}
# or
if not expr {
    ...
}
```
  

### 🔄 Loops 🔄  
**While**  
```java
while (condition) {
    ...
}
```
You can also write the condition whitout parentheses.
```java
while condition {
    ...
}
```
**Do-While** 
```java
do {
    ...
} while (condition);
```
You can also write the condition whitout parentheses and semicolon.
```java
do {
    ...
} while condition
```
  
**For**
```java
for (init; condition; iteration-step) {
    ...
}
```
  
You can also write the condition whitout parentheses.
```java
for init; condition; iteration-step {
    ...
}
```
  
  
### 🚫 Break & Continue ➡️
```java
# You can also write them without a semicolon
break;
continue;
```
  
  
### 🛫 Go to 🛬
```java
label name:
goto name;
```
You can also write them without punctuations marks.
```java
label name
goto name
```
  

### 💭 Comments 💭
**Inline**
```java
# You can write an inline comment using hash character.
```
  
**Multiline & Wrapped**
```java
##
You can write a multiline
comment using two hash characters.
##

## You can write a wrapped comment using two hash characters. ##
```
  
#### For example
```java
# It is right ✅
var:int ## You can write in this space anything you want ## foo = 0;
```
  
  
### 🔡 Functions 🔡
**Declaration & Initialization**  
```java
fun:type name(parameters) {
    code

    return something;
    # or
    ret something;
}
```
  
**Usage**  
```java
var:type variableName = functionName(parameters);
# or if it is a void function
functionName(parameters);
```
  
  
### 🦸 Super Power 🦸  
**⚠️ When you use "Super Power" functions of Vibex, the compiler will not check the code within them. ⚠️**  
  
**Write in C++**
```cpp
CPP
    // Between CPP and # you can write all the C++ code you want
    cout << "With great power comes great responsibility.";
#
```
  
**Write in ASM**
```cpp
ASM
    // Between ASM and # you can write all the Assembly code you want
    "movl $1, %%eax\n"
    "movl $1, %%ebx\n"
    "movl $hello, %%ecx\n"
    "movl $13, %%edx\n"
    "int $0x80\n"
    :
    : "r" ("With great power comes great responsibility.")
    : "%eax", "%ebx", "%ecx", "%edx"
#
```
  
  
### Notes
- You also can write all the keywords in upper case;
  
  
## Roadmap 🛣️
- Arrays n-dimensional;
- Casting;
- Constants;
- Classes;
- Exceptions;
- Increment & Decrement;
- Pointers & References;
- Strings concatenation during output.
  
  
## Changelog Preview 📰
**Development Version 0.1.4.4**
- Various optimizations.
  
**Development Version 0.1.4.3**
- Fixed a bug in function declaration and in return keyword;
- Minor improvements.
  
**All versions**
- Read more [here](./CHANGELOG.md).