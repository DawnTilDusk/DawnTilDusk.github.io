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
    bool inNumber = false;  // ����Ƿ����ڴ�������
    bool hasNonZero = false; // ��ǵ�ǰ�������Ƿ����з�������
    while (cin.get(s) && s != '\n') {
        if (isDigit(s)) {
            if (!inNumber) {
                // ��ʼ�µ�����
                inNumber = true;
                hasNonZero = false;
                if (s != '0') {
                    printf("%c", s);
                    hasNonZero = true;
                }
            } else {
                // ������ǰ����
                if (hasNonZero || s != '0') {
                    printf("%c", s);
                    hasNonZero = true;
                }
            }
        } else {
            if (inNumber) {
                // ���ֽ���
                if (!hasNonZero) {
                    // ����ȫ������
                    printf("0");
                }
                printf("\n");
                inNumber = false;
            }
        }
    }
    // ���������ֽ�β�����
    if (inNumber) {
        if (!hasNonZero) {
            printf("0");
        }
        printf("\n");
    }
    return 0;
}
