import { T, sans } from "../theme";
import FeedbackBubble from "./FeedbackBubble";

export default function Card({ children, title, sub, flex, style, pageId, elementId, round }) {
  const hasFeedback = pageId && elementId;

  return (
    <div
      style={{
        flex: flex || 1,
        background: T.surface,
        border: `1px solid ${T.border}`,
        borderRadius: 10,
        padding: "18px 20px",
        ...style,
      }}
    >
      {(title || hasFeedback) && (
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
          <div style={{ flex: 1 }}>
            {title && (
              <div style={{ fontWeight: 600, fontSize: 14, color: T.text, fontFamily: sans, marginBottom: sub ? 0 : 4 }}>
                {title}
              </div>
            )}
            {sub && (
              <div style={{ fontSize: 12, color: T.textMuted, marginBottom: 12 }}>
                {sub}
              </div>
            )}
          </div>
          {hasFeedback && (
            <FeedbackBubble pageId={pageId} elementId={elementId} round={round} />
          )}
        </div>
      )}
      {!title && !hasFeedback && sub && (
        <div style={{ fontSize: 12, color: T.textMuted, marginBottom: 12 }}>
          {sub}
        </div>
      )}
      {children}
    </div>
  );
}
