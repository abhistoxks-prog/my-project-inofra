export interface Agent {
  name: string;
  description: string;
  status: 'idle' | 'running' | 'error' | 'success';
  last_updated: string | null;
}

export interface FeedItem {
  title: string;
  link: string;
  published: string;
  source: string;
  summary: string;
  type: 'news' | 'market';
}

export interface WeatherDay {
  date: string;
  temp_max: number | null;
  temp_min: number | null;
  precipitation: number | null;
}

export interface WeatherData {
  current: {
    temperature: number | null;
    wind_speed: number | null;
    weather_description: string;
    weather_code: number;
  };
  daily: WeatherDay[];
  location: string;
}

export interface MarketIndex {
  name: string;
  value: number;
  change: number;
  change_percent: number;
}

export interface MarketData {
  indices: MarketIndex[];
  indices_note: string;
  news: FeedItem[];
}

export interface Config {
  topics: string[];
  location: { lat: number; lon: number; name: string };
  refresh_interval: number;
}
