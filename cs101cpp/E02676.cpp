#include <cstdio>
using namespace std;
int a[100001];
int main(){
	int n;
	scanf("%d", &n);
	int cnt1, cnt5, cnt10;
	cnt1 = cnt5 = cnt10 = 0;
	for(int i=1; i<=n; i++){
		scanf("%d", &a[i]);
		if(a[i] == 1) cnt1++;
		else if(a[i] == 5) cnt5++;
		else if(a[i] == 10) cnt10++;
	}
	printf("%d\n%d\n%d\n", cnt1, cnt5, cnt10);
	return 0;
}
