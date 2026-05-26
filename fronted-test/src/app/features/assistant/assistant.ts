import { Component, ViewChild, ElementRef, ChangeDetectorRef, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AssistantService } from '../../service/AssistantService/assistant.service';

interface Message {
  role: 'user' | 'bot';
  text: string;
}

@Component({
  selector: 'app-assistant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './assistant.html',
  styleUrl: './assistant.scss'
})
export class AssistantComponent {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;

  isChatOpen = false;
  isLoading = false;
  userInput = '';
  messages: Message[] = [];

  private publicRoutes = ['/auth', '/login', '/register', '/forgot-password', '/reset-password'];

  constructor(
    private assistantService: AssistantService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private ngZone: NgZone
  ) {
    window.addEventListener('openChat', () => {
      this.ngZone.run(() => {
        this.isChatOpen = true;
        this.cdr.detectChanges();
      });
    });
  }

  get showChat(): boolean {
    return !this.publicRoutes.some(route => this.router.url.startsWith(route));
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
    this.cdr.detectChanges();
    this.scrollToBottom();

    this.assistantService.sendMessage(text, this.getToken())
      .subscribe({
        next: (res) => {
          this.ngZone.run(() => {
            this.messages.push({ role: 'bot', text: res.response });
            this.isLoading = false;
            this.cdr.detectChanges();
            this.scrollToBottom();
          });
        },
        error: () => {
          this.ngZone.run(() => {
            this.messages.push({ role: 'bot', text: 'Error al conectar con el asistente. Intenta de nuevo.' });
            this.isLoading = false;
            this.cdr.detectChanges();
            this.scrollToBottom();
          });
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