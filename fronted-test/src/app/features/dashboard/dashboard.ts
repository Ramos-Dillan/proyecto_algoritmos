import { CommonModule } from '@angular/common';
import { Component, OnInit, OnChanges, SimpleChanges, Input, ChangeDetectorRef } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartData, ChartType } from 'chart.js';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss'],
})
export class Dashboard implements OnInit, OnChanges {

  @Input() refresh: number = 0;

  loading: boolean = false;

  summary = {
    totalUsers: 0,
    totalProducts: 0,
    totalLabs: 0,
    totalGroups: 0,
    activeProducts: 0,
    inactiveProducts: 0
  };

  lineChartType: ChartType = 'line';
  barChartType: ChartType = 'bar';
  doughnutChartType: ChartType = 'doughnut';

  lineChartData: ChartData<'line'> = {
    labels: [],
    datasets: []
  };

  barChartData: ChartData<'bar'> = {
    labels: [],
    datasets: []
  };

  // 🔥 NUEVO: categories
  categoriesChartData: ChartData<'bar'> = {
    labels: [],
    datasets: []
  };

  doughnutChartData: ChartData<'doughnut'> = {
    labels: [],
    datasets: []
  };

  chartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false
  };

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['refresh']) {
      this.loadDashboard();
    }
  }

  loadDashboard() {

    this.loading = true;

    const token = localStorage.getItem('token');

    fetch('http://127.0.0.1:5000/dashboard/summary', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(res => {

        setTimeout(() => {

          const data = res.data;

          if (!data) {
            this.loading = false;
            this.cdr.detectChanges();
            return;
          }

          this.summary = {
            totalUsers: data.totalUsers ?? 0,
            totalProducts: data.totalProducts ?? 0,
            totalLabs: data.totalLabs ?? 0,
            totalGroups: data.totalGroups ?? 0,
            activeProducts: data.activeProducts ?? 0,
            inactiveProducts: data.inactiveProducts ?? 0
          };

          // LINE
          this.lineChartData = {
            labels: ['Usuarios', 'Productos', 'Labs', 'Grupos'],
            datasets: [{
              data: [
                data.totalUsers,
                data.totalProducts,
                data.totalLabs,
                data.totalGroups
              ],
              label: 'Sistema'
            }]
          };

          // DOUGHNUT
          this.doughnutChartData = {
            labels: ['Activos', 'Inactivos'],
            datasets: [{
              data: [
                data.activeProducts,
                data.inactiveProducts
              ]
            }]
          };

          // BAR (GRUPOS)
          this.barChartData = {
            labels: data.chart?.groups || [],
            datasets: [{
              data: data.chart?.products || [],
              label: 'Productos por grupo'
            }]
          };

          // 🔥 NUEVO: BAR (CATEGORIES)
          this.categoriesChartData = {
            labels: data.categoriesChart?.categories || [],
            datasets: [{
              data: data.categoriesChart?.products || [],
              label: 'Productos por categoría'
            }]
          };

          this.loading = false;
          this.cdr.detectChanges();

        }, 0);

      })
      .catch(err => {
        console.log('Error dashboard:', err);
        this.loading = false;
        this.cdr.detectChanges();
      });
  }
}