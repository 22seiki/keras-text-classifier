#include <iostream>

using namespace std;

#define MAX 3

int calc(int s[MAX][MAX]);
void solve(int a[MAX][MAX], int b[MAX]);
int ans(int s[MAX][MAX]);

int N[MAX][MAX];

int main(){
    int a[MAX][MAX], b[MAX];

    for(int i=0; i<MAX; i++){
        for(int j=0; j<MAX; j++){
            cin >> a[i][j];
            N[i][j] = 0;
        }
        cin >> b[i];
    }
    /*
    for(int i=0; i<MAX; i++){
        cout << "| ";
        for(int j=0; j<MAX; j++){
            printf("%3d ", a[i][j]);
        }
        printf("| = %3d\n", b[i]);
    }*/

    if(calc(a) != 0){
        solve(a, b);
    }else{
        for(int i=0; i<MAX; i++){
            cout << "x[" << i+1 << "] = " << 0 << endl;
        }
    }
    return 0;
}

void solve(int a[MAX][MAX], int b[MAX]){
    int x[MAX], y[MAX][MAX];

    for(int i=0; i<MAX; i++){
        for(int j=0; j<MAX; j++){
            y[i][j] = a[i][j];
        }
    }

    for(int i=0; i<MAX; i++){
        for(int j=0; j<MAX; j++){
            y[j][i] = b[j];
        }
        x[i] = calc(y) / calc(a);
        cout << "x[" << i+1 << "] = " << x[i] << endl;
        for(int j=0; j<MAX; j++){
            y[j][i] = a[j][i];
        }
    }
}

int calc(int s[MAX][MAX]){
    int ans;
    
    /*
    for(int i=0; i<MAX; i++){
        cout << "| ";
        for(int j=0; j<MAX; j++){
            printf("%3d ", s[i][j]);
        }
        printf("|\n");
    }*/

    ans = s[0][0]*s[1][1]*s[2][2]
        + s[1][0]*s[2][1]*s[0][2]
        + s[2][0]*s[0][1]*s[1][2]
        - s[0][2]*s[1][1]*s[2][0]
        - s[0][1]*s[1][0]*s[2][2]
        - s[0][0]*s[1][2]*s[2][1];

    cout << ans << endl;
    return ans;
}

int ans(int s[MAX][MAX]){
}