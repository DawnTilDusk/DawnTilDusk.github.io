#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define MAX_LEN 80

int main() {
    char str[MAX_LEN + 1]; // +1 for null terminator
    
    // ��ȡ������
    fgets(str, sizeof(str), stdin);
    
    // �Ƴ����ܵĻ��з�
    str[strcspn(str, "\n")] = '\0';
    
    // ����ÿ���ַ�
    for (int i = 0; str[i] != '\0'; i++) {
        if (isupper(str[i])) {
            str[i] = tolower(str[i]);
        } else if (islower(str[i])) {
            str[i] = toupper(str[i]);
        }
        // ����ĸ�ַ����ֲ���
    }
    
    // ������
    printf("%s\n", str);
    
    return 0;
}
