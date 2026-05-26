import { Component, ViewChild, ElementRef } from '@angular/core';
import { RouterOutlet, RouterLink, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
interface Message {
  role: 'user' | 'bot';
  text: string;
}

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, RouterLink, CommonModule, FormsModule],
  templateUrl: './shell.html',
  styleUrl: './shell.scss'
})
export class ShellComponent {

  @ViewChild('messagesContainer') messagesContainer!: ElementRef;

  isSidebarClosed = false;
  isDropdownOpen = false;
  isChatOpen = false;
  isLoading = false;
  userInput = '';
  messages: Message[] = [];

  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient, private router: Router) {}

  toggleSidebar() {
    this.isSidebarClosed = !this.isSidebarClosed;
  }

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  toggleChat() {
    this.isChatOpen = !this.isChatOpen;
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
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