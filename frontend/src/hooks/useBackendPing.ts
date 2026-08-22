'use client';
import { useState, useEffect } from 'react';

export function useBackendPing(url: string = 'http://127.0.0.1:8000') {
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    const checkPing = async () => {
      try {
        const res = await fetch(`${url}/api/v1/health`, { cache: 'no-store' });
        if (res.ok) setIsOnline(true);
        else setIsOnline(false);
      } catch {
        setIsOnline(false);
      }
    };
    
    checkPing();
    interval = setInterval(checkPing, 5000);
    
    return () => clearInterval(interval);
  }, [url]);

  return isOnline;
}
