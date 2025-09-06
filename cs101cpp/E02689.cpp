#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define MAX_LEN 80

int main() {
    char str[MAX_LEN + 1]; // +1 for null terminator
    
    // 读取输入行
    fgets(str, sizeof(str), stdin);
    
    // 移除可能的换行符
    str[strcspn(str, "\n")] = '\0';
    
    // 处理每个字符
    for (int i = 0; str[i] != '\0'; i++) {
        if (isupper(str[i])) {
            str[i] = tolower(str[i]);
        } else if (islower(str[i])) {
            str[i] = toupper(str[i]);
        }
        // 非字母字符保持不变
    }
    
    // 输出结果
    printf("%s\n", str);
    
    return 0;
}
