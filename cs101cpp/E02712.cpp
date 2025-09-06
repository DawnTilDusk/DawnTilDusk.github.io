#include <iostream>
#include <cstdio>
#include <cmath>
using namespace std;

int M[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

int getDay(int sm, int sd, int em, int ed){
	int cnt = 0;
	if(sm+1 <= em-1){
		for(int i=sm+1; i<=em-1; i++)
			cnt += M[i];
		return cnt + M[sm] - sd + ed;
	}
	else if(sm+1 == em)
		return M[sm] - sd + ed;
	else return ed - sd;
}

int main(){
	cout<< getDay(1, 1, 3, 3);
	int m;
	scanf("%d", &m);
	while(m){
		m--;
		int sm, sd, em, ed, b;
		scanf("%d%d%d%d%d", &sm, &sd, &b, &em, &ed);
		int n = getDay(sm, sd, em, ed);
		long long ans = pow(2, n)*b;
//		cout << n << endl;
		printf("%lld\n", ans);	
	}
	return 0;
}
