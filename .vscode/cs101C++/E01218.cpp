#include <cstdio>
using namespace std;
bool door[1000000];
int main(){
    for(int i = 1; i <= 1e6; i++) 
        door[i] = false;
    int m, n;
    scanf("%d", &m);
    for (int i = 1; i <= m; i++) {
        scanf("%d", &n);
        for(int i = 1; i<= n; i++){
            for(int j = 1; j <= n; j += i){
                door[j] = !door[j];
            }
        }
    }
    int cnt = 0;
    for(int i = 1; i<=m; i++){
        cnt += door[i];
    }
    printf("%d\n", cnt);
    return 0;
}