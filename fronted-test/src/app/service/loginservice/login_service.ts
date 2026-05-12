import { Injectable, computed, signal } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { tap, map, catchError } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import { throwError } from 'rxjs';

type LoginApiResponse = {
  status: 'success' | 'error';
  message?: string;
  data?: {
    access_token?: string;
    user?: any;
  };
};

@Injectable({ providedIn: 'root' })
export class LoginService {

  // 🔥 CORREGIDO AQUÍ
  private readonly TOKEN_KEY = 'token';
  private readonly USER_KEY = 'my_user';

  private _token = signal<string | null>(this.getToken());
  token = computed(() => this._token());

  private _user = signal<any | null>(this.getUser());
  user = computed(() => this._user());

  constructor(private http: HttpClient) {}

  login(email: string, password: string) {
    return this.http
      .post<LoginApiResponse>(`${environment.apiBaseURL}/auth/login`, {
        email: email,
        password: password
      })
      .pipe(
        tap((res) => {
          console.log('LOGIN RESPONSE =>', res);
        }),

        map((res) => {
          const token = res?.data?.access_token ?? null;
          const user = res?.data?.user ?? null;

          if (!token) {
            throw new HttpErrorResponse({
              status: 401,
              statusText: res?.message || 'Credenciales incorrectas'
            });
          }

          this.setToken(token);

          if (user) {
            const fixedUser = {
              ...user,
              role: user.role ?? 'estudiante'
            };

            this.setUser(fixedUser);
          }

          return { token, user };
        }),

        catchError((err: HttpErrorResponse) => {
          console.error('ERROR LOGIN SERVICE:', err);
          return throwError(() => err);
        })
      );
  }

  register(
    username: string,
    email: string,
    identification: string,
    password: string
  ) {
    return this.http
      .post<LoginApiResponse>(`${environment.apiBaseURL}/auth/create`, {
        username,
        email,
        identification,
        password
      })
      .pipe(
        tap((res) => {
          console.log('REGISTER RESPONSE =>', res);
        }),

        map((res) => {
          if (res?.status === 'error') {
            throw new HttpErrorResponse({
              status: 400,
              statusText: res?.message || 'Error en registro'
            });
          }

          return res;
        }),

        catchError((err: HttpErrorResponse) => {
          console.error('ERROR REGISTER SERVICE:', err);
          return throwError(() => err);
        })
      );
  }

  // ✅ FORGOT PASSWORD
  forgotPassword(email: string) {
    return this.http.post<any>(
      `${environment.apiBaseURL}/auth/forgot-password`,
      { email }
    );
  }

  // ✅ RESET PASSWORD
  resetPassword(token: string, password: string) {
    return this.http.post<any>(
      `${environment.apiBaseURL}/auth/reset-password`,
      {
        token,
        password
      }
    );
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getUser(): any | null {
    const raw = localStorage.getItem(this.USER_KEY);
    return raw ? JSON.parse(raw) : null;
  }

  private setUser(user: any) {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    this._user.set(user);
  }

  private setToken(token: string) {
    localStorage.setItem(this.TOKEN_KEY, token);
    this._token.set(token);
  }

  private clearToken() {
    localStorage.removeItem(this.TOKEN_KEY);
    this._token.set(null);
  }

  private clearUser() {
    localStorage.removeItem(this.USER_KEY);
    this._user.set(null);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  logout() {
    this.clearToken();
    this.clearUser();
  }
}