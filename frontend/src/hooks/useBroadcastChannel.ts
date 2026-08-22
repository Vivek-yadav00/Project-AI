'use client';
import { useEffect, useCallback, useRef } from 'react';

export function useBroadcastChannel(channelName: string, onMessage: (msg: any) => void) {
  const channelRef = useRef<BroadcastChannel | null>(null);

  useEffect(() => {
    const bc = new BroadcastChannel(channelName);
    channelRef.current = bc;
    bc.onmessage = (event) => {
      onMessage(event.data);
    };
    return () => {
      bc.close();
      channelRef.current = null;
    };
  }, [channelName, onMessage]);

  const postMessage = useCallback((msg: any) => {
    if (channelRef.current) {
      channelRef.current.postMessage(msg);
    }
  }, []);

  return { postMessage };
}
