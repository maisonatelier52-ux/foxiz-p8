import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Our Authors | Foxiz News",
    description: "Meet the expert journalists and contributors behind Foxiz's in-depth financial analysis and market insights.",
    openGraph: {
        title: "Our Authors | Foxiz News",
        description: "Behind every story: meet the Foxiz global editorial team.",
        url: "https://foxiz-news.com/authors",
        siteName: "Foxiz",
        images: [
            {
                url: "/images/news/markets-1.webp",
                width: 1200,
                height: 630,
                alt: "Foxiz Authors",
            }
        ],
        type: "website",
    },
    twitter: {
        card: "summary_large_image",
        title: "Our Authors | Foxiz News",
        description: "Meet the voices shaping the future of financial journalism at Foxiz.",
        images: ["/images/news/markets-1.webp"],
    },
};

export default function AuthorsLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return <>{children}</>;
}
