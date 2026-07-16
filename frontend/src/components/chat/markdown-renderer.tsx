import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * Renders assistant markdown answers (PRD F1) with the design system's
 * typography. GitHub-flavored markdown enables lists, tables and emphasis.
 */
export function MarkdownRenderer({ content }: { content: string }) {
  return (
    <div className="flex flex-col gap-3 text-base leading-relaxed text-text-primary">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children }) => <p>{children}</p>,
          strong: ({ children }) => (
            <strong className="font-semibold">{children}</strong>
          ),
          ul: ({ children }) => (
            <ul className="ml-5 flex list-disc flex-col gap-1">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="ml-5 flex list-decimal flex-col gap-1">{children}</ol>
          ),
          li: ({ children }) => <li className="pl-1">{children}</li>,
          h1: ({ children }) => (
            <h3 className="text-lg font-semibold">{children}</h3>
          ),
          h2: ({ children }) => (
            <h4 className="text-base font-semibold">{children}</h4>
          ),
          h3: ({ children }) => (
            <h5 className="text-base font-semibold">{children}</h5>
          ),
          a: ({ children, href }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent underline underline-offset-2"
            >
              {children}
            </a>
          ),
          code: ({ children }) => (
            <code className="rounded-sm bg-surface-inset px-1 py-0.5 font-mono text-sm">
              {children}
            </code>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
