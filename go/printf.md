# fmt.printf

```
package main

import "fmt"
import "os"

type point struct {
	x, y int
}

func main() {
	p := point{1, 2}
	//输出结构体的一个实例
	fmt.Printf("%v\n", p) //{1 2}
	//输出实例将包括字段名
	fmt.Printf("%+v\n", p) //{x:1 y:2}
	//输出实例的语法表示
	fmt.Printf("%#v\n", p) //main.point{x:1, y:2}
	//输出值的类型
	fmt.Printf("%T\n", p) //main.point
	//输出布尔值
	fmt.Printf("%t\n", true) //true
	//输出二进制
	fmt.Printf("%b\n", 14) //1110
	//输出十进制
	fmt.Printf("%d\n", 123) //123
	//输出十六进制
	fmt.Printf("%x\n", 456) //1c8
	//输出字符
	fmt.Printf("%c\n", 33) //!
	//输出字符串
	fmt.Printf("%s\n", "\"string\"") //"string"
	//输出浮点数
	fmt.Printf("%f\n", 78.9) //78.900000
	//输出科学记数法形式
	fmt.Printf("%e\n", 123400000.0) //1.234000e+08
	fmt.Printf("%E\n", 123400000.0) //1.234000E+08
	//输出带双引号形式
	fmt.Printf("%q\n", "\"string\"") //"\"string\""
	//输出十六进制的字符串形式
	fmt.Printf("%x\n", "hex this") //6865782074686973
	//输出指针
	fmt.Printf("%p\n", &p) //0xc000080010
	//输出带宽度的十进制形式
	fmt.Printf("|%6d|%6d|\n", 12, 345) //|    12|   345|
	//输出带宽度精度的浮点数形式
	fmt.Printf("|%6.2f|%6.2f|\n", 1.2, 3.45) //|  1.20|  3.45|
	//输出带宽度精度左对齐的浮点数形式
	fmt.Printf("|%-6.2f|%-6.2f|\n", 1.2, 3.45) //|1.20  |3.45  |
	//输出带宽度的字符串形式
	fmt.Printf("|%6s|%6s|\n", "foo", "b") //|   foo|     b|
	//输出带宽度左对齐的字符串形式
	fmt.Printf("|%-6s|%-6s|\n", "foo", "b") //|foo   |b     |
	//返回指定形式的值
	s := fmt.Sprintf("a %s", "string")
	fmt.Println(s) //a string
	//重定向指定形式的值
	fmt.Fprintf(os.Stderr, "an %s\n", "error") //an error
}
```