#### golang json
```cassandraql
package main
 
import (
    "encoding/json"
    "fmt"
    "os"
)
 
type ConfigStruct struct {
    Host              string   `json:"host"`
    Port              int      `json:"port"`
    AnalyticsFile     string   `json:"analytics_file"`
    StaticFileVersion int      `json:"static_file_version"`
    StaticDir         string   `json:"static_dir"`
    TemplatesDir      string   `json:"templates_dir"`
    SerTcpSocketHost  string   `json:"serTcpSocketHost"`
    SerTcpSocketPort  int      `json:"serTcpSocketPort"`
    Fruits            []string `json:"fruits"`
}
 
type Other struct {
    SerTcpSocketHost string   `json:"serTcpSocketHost"`
    SerTcpSocketPort int      `json:"serTcpSocketPort"`
    Fruits           []string `json:"fruits"`
}
 
func main() { 
    jsonStr := `{"host": "http://localhost:9090","port": 9090,"analytics_file": "","static_file_version": 1,"static_dir": "E:/Project/goTest/src/","templates_dir": "E:/Project/goTest/src/templates/","serTcpSocketHost": ":12340","serTcpSocketPort": 12340,"fruits": ["apple", "peach"]}`
 
    //json str >> map
    var dat map[string]interface{}
    if err := json.Unmarshal([]byte(jsonStr), &dat); err == nil {
        fmt.Println("============== json str >> map ==============")
        fmt.Println(dat)
        fmt.Println(dat["host"])
    }
 
    //json str >> struct
    var config ConfigStruct
    if err := json.Unmarshal([]byte(jsonStr), &config); err == nil {
        fmt.Println("============== json str >> struct ==============")
        fmt.Println(config)
        fmt.Println(config.Host)
    }
 
    //json str >> struct
    var part Other
    if err := json.Unmarshal([]byte(jsonStr), &part); err == nil {
        fmt.Println("============== json str >> struct ==============")
        fmt.Println(part)
        fmt.Println(part.SerTcpSocketPort)
    }
 
    //struct >> json str
    if b, err := json.Marshal(config); err == nil {
        fmt.Println("============== struct >> json str ==============")
        fmt.Println(string(b))
    }
 
    //map >> json str
    fmt.Println("============== map >> json str ==============")
    enc := json.NewEncoder(os.Stdout)
    enc.Encode(dat)
 
    //array >> json str
    arr := []string{"hello", "apple", "python", "golang", "base", "peach", "pear"}
    lang, err := json.Marshal(arr)
    if err == nil {
        fmt.Println("============== array >> json str ==============")
        fmt.Println(string(lang))
    }
 
    //json >> []string
    var wo []string
    if err := json.Unmarshal(lang, &wo); err == nil {
        fmt.Println("============== json >> []string ==============")
        fmt.Println(wo)
    }
}
```