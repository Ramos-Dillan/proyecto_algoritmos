import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap, map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
 
export interface User {
  id: number;
  identification: string;
  email: string;
  full_name: string;
  is_active: number;
}
 
type GetUserApiResponse = {
  status: 'success' | 'error';
  message?: string;
  data?: {
    users?: User[];
  };
};
 
@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiBaseUrl = `${environment.apiBaseURL}/users`;
 
  constructor(private http: HttpClient) {}
 
  getAllUsers() {
    return this.http.get<GetUserApiResponse>(`${this.apiBaseUrl}/getAll`).pipe(
      tap(response => {
        if (response.status === 'error') {
          console.error('Error fetching users:', response.message);
        }
      }),
      map(response => response.data?.users || [])
    );
  }
}