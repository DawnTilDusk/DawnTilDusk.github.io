#include <iostream>
#include <cstdio>
#include <cstring>
#include <iomanip>
using namespace std;

int a[7][7];

bool swap(int n, int m){
	if(n>4 || n<0 || m>4 || m<0)
		return 0;
	else
		for(int i=1; i<=5; i++){
			int tmp;
			tmp = a[n+1][i];
			a[n+1][i] = a[m+1][i];
			a[m+1][i] = tmp;
		}
	return 1;
}		

int main(){
	for(int i=1; i<=5; i++)
		for(int j=1; j<=5; j++)
			scanf("%d", &a[i][j]);
	int n, m;
	scanf("%d%d", &n, &m);
	if(swap(n, m))
		for(int i=1; i<=5; i++){
			for(int j=1; j<=5; j++)
				cout << setw(4) << a[i][j];
            cout << endl;
		}
	else printf("error\n");
	return 0;
}
