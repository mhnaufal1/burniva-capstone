import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import useAuthStore from "../store/auth/useAuthStore";
import { ROUTES } from "../utils/constants";

const IDLE_TIMEOUT_MS = 60 * 60 * 1000; // 60 minutes
const CHECK_INTERVAL_MS = 60 * 1000; // Check token every 1 minute

export const useAuthCheck = () => {
  const { token, clearAuth, isAuthenticated } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated || !token) return;

    let idleTimer;
    let tokenCheckInterval;

    const handleLogout = (reason) => {
      console.log(`Logging out due to: ${reason}`);
      clearAuth();
      navigate(ROUTES.LOGIN, { replace: true });
    };

    const checkTokenExpiration = () => {
      try {
        const decoded = jwtDecode(token);
        const currentTime = Date.now() / 1000; // in seconds

        if (decoded.exp < currentTime + 5) {
          handleLogout("token_expired");
        }
      } catch (error) {
        console.error("Invalid token:", error);
        handleLogout("invalid_token");
      }
    };

    const resetIdleTimer = () => {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => {
        handleLogout("idle_timeout");
      }, IDLE_TIMEOUT_MS);
    };

    checkTokenExpiration();
    resetIdleTimer();

    tokenCheckInterval = setInterval(checkTokenExpiration, CHECK_INTERVAL_MS);

    const events = [
      "mousedown",
      "mousemove",
      "keypress",
      "scroll",
      "touchstart",
    ];
    events.forEach((event) => {
      window.addEventListener(event, resetIdleTimer, { passive: true });
    });

    return () => {
      clearTimeout(idleTimer);
      clearInterval(tokenCheckInterval);
      events.forEach((event) => {
        window.removeEventListener(event, resetIdleTimer);
      });
    };
  }, [token, isAuthenticated, clearAuth, navigate]);
};
