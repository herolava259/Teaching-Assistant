# **Transfer to Go programming language for build performance service (Go4Fun^-^)** (refer from w3school)

## **Chapter I. Introduction**
### 1. What is Go?
- Go is a cross-platform, open-source programming language 
- Go can be used to create high performance applications 
- Go is a fast, statically typed, compiled language known for its simplicity and efficiency
- Go was developed at Google by Robert Griesemer, Rob Pike, and Ken Thompson in 2007
- Go's syntax is similar to C++

### 2. What is Go used for? 
- Web development (server-side)
- Developing network-based programs 
- Developing cross-platform enterprise applications
- Cloud-native development 

### 3. Features
- Statically typed 
- Fast run time 
- Compiled 
- Fast compile time 
- Support concurrency through goroutines and channel
- Has automatic garbage collection 
- Does not support classes and objects 
- Does not support inheritance (KISS)

## Chapter II. Installation and setup environment for programming 
### 1. Go Install 
- Reference Link [Go: Download and Install](https://go.dev/doc/install)
- Install Utility in IDE: 
    * Using Visual Studio Code 
    * Install extension **Go** to the ide support to syntax 
    * press **Ctrl + Shift + X** to open to Extension
    * Pressinf **Ctrl + Shift + P** to open the command 
    * Run Go: Install/Update Tools command 
    * Select all provided tools and Click OK
### 2. Go Quickstart (simple)
- Launch the VS Code editor 
- Open up a terminal window and type: 
```bash
go mod init example.com/hello
```
- Create a new file: helloworld.go
- Type a following code:
```go
package main
import ("fmt")

func main() {
  fmt.Println("Hello World!")
}
```
- Type on terminal: 
```bash
go run .\helloworld.go
```

## Chapter III. Go syntax 
1.Go Syntax
A Go file consists of the following parts:

- Package declaration
- Import packages
- Functions
- Statements and expressions
Look at the following code, to understand it better:
```go
package main
import ("fmt")

func main() {
  fmt.Println("Hello World!")
}
```
Example explained
Line 1: In Go, every program is part of a package. We define this using the package keyword. In this example, the program belongs to the main package.

Line 2: import ("fmt") lets us import files included in the fmt package.

Line 3: A blank line. Go ignores white space. Having white spaces in code makes it more readable.

Line 4: func main() {} is a function. Any code inside its curly brackets {} will be executed.

Line 5: fmt.Println() is a function made available from the fmt package. It is used to output/print text. In our example it will output "Hello World!".
2. Comments

## Chapter IV. Go structure

