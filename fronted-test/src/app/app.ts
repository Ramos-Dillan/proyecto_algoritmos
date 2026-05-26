import { Component, signal, ViewChild, ElementRef } from '@angular/core';
import { RouterOutlet, RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

interface Message {
  role: 'user' | 'bot';
  text: string;
}

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterModule, CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('fronted-test');

  @ViewChild('messagesContainer') messagesContainer!: ElementRef;

  isChatOpen = false;
  isLoading = false;
  userInput = '';
  messages: Message[] = [];

  private apiUrl = 'http://localhost:5000';
  private publicRoutes = ['/auth', '/login', '/register', '/forgot-password', '/reset-password'];

  constructor(private http: HttpClient, private router: Router) {
    window.addEventListener('openChat', () => {
      this.isChatOpen = true;
    });
  }

  get showChat(): boolean {
    return !this.publicRoutes.some(route =>
      this.router.url.startsWith(route)
    );
  }

  toggleChat() {
    this.isChatOpen = !this.isChatOpen;
  }

  getToken(): string {
    return localStorage.getItem('token') || '';
  }

  sendMessage() {
    const text = this.userInput.trim();
    if (!text || this.isLoading) return;

    this.messages.push({ role: 'user', text });
    this.userInput = '';
    this.isLoading = true;
    this.scrollToBottom();

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.getToken()}`
    });

    this.http.post<any>(`${this.apiUrl}/assistant/chat`, { message: text }, { headers })
      .subscribe({
        next: (res) => {
          this.messages.push({ role: 'bot', text: res.data.response });
          this.isLoading = false;
          this.scrollToBottom();
        },
        error: () => {
          this.messages.push({ role: 'bot', text: 'Error al conectar con el asistente. Intenta de nuevo.' });
          this.isLoading = false;
          this.scrollToBottom();
        }
      });
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop =
          this.messagesContainer.nativeElement.scrollHeight;
      }
    }, 100);
  }
}