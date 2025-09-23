#include <iostream>
#include <cstdio>
#include <cmath>
#include <algorithm>
#include <windows.h>
using namespace std;

#define  ll long double

ll a[1001][1001];

bool equal(ll a, ll b) {
    return fabs(a - b) < 1e-9; // 使用一个小的阈值来比较浮点数
}

void init(int m, int n){
    for(int i=1; i<=m; i++)
        for(int j=0; j<=n; j++)
            if(equal(a[i][j], 0))
                a[i][j] = 0;
}

void exchange_row(int r1, int r2, int n) {
    for (int i = 1; i <= n; i++) {
        swap(a[r1][i], a[r2][i]);
    }
}

void scale_row(int r, ll k, int n) {
    for (int i = 1; i <= n; i++) 
        a[r][i] *= k;
}

void add_multiple_row(int r1, int r2, ll k, int n) {
    for (int i = 1; i <= n; i++) 
        a[r1][i] += a[r2][i] * k;
}

void print_matrix(int m, int n) {
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            printf("%.2Lf ", a[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

void ref(int m, int n){
    int entry = 1;
    for(int r=1; r<=m; r++){
/*        while(entry <= n && equal(a[r][entry], 0)){
            for(int i=r+1; i<=m; i++){
                if(!equal(a[i][entry], 0)){
                    exchange_row(i, r, n);
                    cout << "REF step " << r << ":\n";
                    print_matrix(m, n);
                    break;
                }
            }
            if(equal(a[r][entry], 0))
                entry++;
            else break;
        }*/
        while(entry <= n){
            int pivot = 0; ll max = 0;
            for(int i=r; i<=n; i++)
                if(fabs(a[i][entry]) > max){
                    max = fabs(a[i][entry]);
                    pivot = i;
                }
            if(pivot != 0 && !equal(max, 0)){
                exchange_row(pivot, r, n);
                break;
            }
            entry++;
        }
        
        if(entry > n) break;
        scale_row(r, 1.0/a[r][entry], n);
        for(int i=r+1; i<=m; i++)
            if(!equal(a[i][entry], 0))
                add_multiple_row(i, r, -a[i][entry], n);
        cout << "REF step " << r << ":\n"<<"entry="<<entry<<"\n";
        print_matrix(m, n);
        entry++;
    }
}

void rref(int m, int n){
    ref(m, n);
    init(m, n);
    for(int r=m; r>=1; r--){
        int entry=1;
        while(entry <= n && equal(a[r][entry], 0))
            entry++;
        for(int i=r-1; i>=1; i--){
            if(a[i][entry] == 0)
                continue;
            add_multiple_row(i, r, -a[i][entry], n);
        }
        cout << "RREF step " << m-r+1 << ":\n";
        print_matrix(m, n);
    }
}

int main(){
    while(1){
        system("cls");
        cout << "Enter matrix size (m n): ";
        int m, n;
        scanf("%d %d", &m, &n);
        cout << "Enter matrix (" << m << "x" << n << "):\n";
        char buf[32];
        for(int i=1; i<=m; i++) {
            for(int j=1; j<=n; j++) {
                scanf("%s", buf);
                if(buf[0] == 'Q' || buf[0] == 'q')
                    return 0;
                sscanf(buf, "%Lf", &a[i][j]);
            }
        }
        printf("\n");
        printf("Original matrix:\n");
        print_matrix(m, n);
        rref(m, n);
        init(m, n);
        print_matrix(m, n);
        cout << "Press any key to continue...\nPress 'Q' to quit anytime.\n";
        getchar(); 
        if(getchar() == 'Q' || getchar() == 'q')
            break;
    }
    return 0;
}

/*
4 5
12    -7    11    -9     5
-9     4    -8     7    -3
-6    11    -7     3    -9
4    -6    10    -5    12

4 5
-0.3500    0.3000    0.3000    0.2000         0
0.1000   -0.9000    0.1500    0.1000         0
0.2500    0.3500   -0.8500    0.3000         0
0    0.2500    0.4000   -0.6000         0

5     6

    0.6476    0.7093    0.4587    0.4162    0.5822    0.1192
    0.6790    0.2362    0.6619    0.8419    0.5407    0.9398
    0.6358    0.1194    0.7703    0.8329    0.8699    0.6456
    0.9452    0.6073    0.3502    0.2564    0.2648    0.4795
    0.2089    0.4501    0.6620    0.6135    0.3181    0.6393
*/