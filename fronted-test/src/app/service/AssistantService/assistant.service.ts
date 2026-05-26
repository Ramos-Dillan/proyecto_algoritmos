import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { map, catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { environment } from '../../../environments/environment';

type AssistantApiResponse = {
  status: 'success' | 'error';
  message?: string;
  data?: {
    response?: string;
    user_message?: string;
  };
};

@Injectable({ providedIn: 'root' })
export class AssistantService {

  constructor(private http: HttpClient) {}

  sendMessage(message: string, token: string) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });

    return this.http
      .post<AssistantApiResponse>(
        `${environment.apiBaseURL}/assistant/chat`,
        { message },
        { headers }
      )
      .pipe(
        map((res) => {
          const response = res?.data?.response ?? null;

          if (!response) {
            throw new HttpErrorResponse({
              status: 400,
              statusText: res?.message || 'Sin respuesta del asistente'
            });
          }

          return {
            response,
            user_message: res?.data?.user_message ?? message
          };
        }),

        catchError((err: HttpErrorResponse) => {
          console.error('ERROR ASSISTANT SERVICE:', err);
          return throwError(() => err);
        })
      );
  }
}