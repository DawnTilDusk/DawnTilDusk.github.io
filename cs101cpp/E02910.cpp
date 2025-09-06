#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <vector>
#include <algorithm>
using namespace std;

bool isDigit(char s) {
    return s >= '0' && s <= '9';
}

int main() {
    char s;
    bool inNumber = false;  // 标记是否正在处理数字
    bool hasNonZero = false; // 标记当前数字中是否已有非零数字
    while (cin.get(s) && s != '\n') {
        if (isDigit(s)) {
            if (!inNumber) {
                // 开始新的数字
                inNumber = true;
                hasNonZero = false;
                if (s != '0') {
                    printf("%c", s);
                    hasNonZero = true;
                }
            } else {
                // 继续当前数字
                if (hasNonZero || s != '0') {
                    printf("%c", s);
                    hasNonZero = true;
                }
            }
        } else {
            if (inNumber) {
                // 数字结束
                if (!hasNonZero) {
                    // 处理全零的情况
                    printf("0");
                }
                printf("\n");
                inNumber = false;
            }
        }
    }
    // 处理以数字结尾的情况
    if (inNumber) {
        if (!hasNonZero) {
            printf("0");
        }
        printf("\n");
    }
    return 0;
}
