#include <cmath>
#include <iostream>
#include <cstdio>
#include <cstring>
using namespace std;

int main(){
	int n, cnt = 0;
	scanf("%d", &n);
	for(int i=1; i<=n; i++){
		int p = i;
		bool flag = 0;
		if(p % 7 == 0) {
			flag = 1;
			continue;
		}
		do{
			if(p != 0 && p%10 == 7) flag = 1;
			p /= 10;
//			cout << p << endl;
		}while(p);
		if(flag == 0)
			cnt += pow(i, 2);
//		cout<<i<<" "<<cnt<<endl;
	}
	printf("%d\n", cnt);
	return 0;
}
