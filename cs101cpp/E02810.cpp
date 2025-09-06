#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
using namespace std;

int main(){
	int n, a, b, c, d;
	scanf("%d", &n);
	for(int a=6; a<=n; a++)
		for(int b=2; b<=n; b++)
			for(int c=b; c<=n; c++)
				if(a*a*a <= c*c*c + b*b*b) break;
				else 
					for(int d=c; d<=n; d++)
						if(a*a*a == b*b*b + c*c*c + d*d*d)
							printf("Cube = %d, Triple = (%d,%d,%d)\n", a, b, c, d);
	return 0;
}
