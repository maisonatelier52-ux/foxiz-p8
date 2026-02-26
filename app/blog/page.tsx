import { Metadata } from "next";
import Header from "../components/layout/Header";
// import Navbar from "../components/layout/Navbar"; // Navbar component not found in codebase
import Footer from "../components/layout/Footer";
import Image from "next/image";
import Link from 'next/link';
import { ChevronRight } from "lucide-react";
import AdvertisementSection from "../components/home/AdvertisementSection";
import MoreNews from "../components/home/MoreNews";
import WhatToRead from "../components/home/WhatToRead";

export const metadata: Metadata = {
    title: "Blog | Foxiz News",
    description: "In-depth analysis, global affairs, and expert insights from Foxiz News.",
    openGraph: {
        title: "Blog | Foxiz News",
        description: "Explore the latest stories and analytical reports from Foxiz.",
        url: "https://foxiz-news.com/blog",
        siteName: "Foxiz",
        type: "website",
    },
};


const blogFeaturedData = {
    mainArticle: {
        title: "How Migration Is Reshaping Borders and Policies",
        category: "GLOBAL AFFAIRS",
        date: "May 13, 2025",
        image: "https://images.unsplash.com/photo-1573164067005-430ecce66376?q=80&w=2069&auto=format&fit=crop",
        slug: "how-migration-is-reshaping-borders-and-policies"
    },
    gridArticles: [
        {
            title: "Global Trade Wars: Winners, Losers, and Long-Term Effects",
            category: "GLOBAL AFFAIRS",
            date: "May 13, 2025",
            image: "https://images.unsplash.com/photo-1541872703-74c5e44368f9?q=80&w=2018&auto=format&fit=crop",
            slug: "global-trade-wars-winners-losers"
        },
        {
            title: "Cybersecurity Becomes the New Frontline of Global Conflict",
            category: "GLOBAL AFFAIRS",
            date: "May 13, 2025",
            image: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop",
            slug: "cybersecurity-new-frontline"
        },
        {
            title: "War-Torn Nation Begins Reconstruction Efforts with International Aid",
            category: "WORLD",
            date: "May 13, 2025",
            image: "https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?q=80&w=2070&auto=format&fit=crop",
            slug: "war-torn-nation-reconstruction"
        },
        {
            title: "Foreign Aid Sparks Debate Over Motives and Impact",
            category: "GLOBAL AFFAIRS",
            date: "May 13, 2025",
            image: "https://images.unsplash.com/photo-1521791136064-7986c2959443?q=80&w=2070&auto=format&fit=crop",
            slug: "foreign-aid-debate"
        }
    ]
};

export default function BlogPage() {
    return (
        <main className="bg-white min-h-screen">
            <Header />
            {/* <Navbar /> */}

            {/* Breadcrumb Section to match other pages */}
            <div className="bg-white border-b border-gray-100">
                <div className="max-w-[1330px] mx-auto px-4 py-4">
                    <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-gray-400">
                        <Link href="/" className="hover:text-red-500 transition-colors">Home</Link>
                        <ChevronRight size={12} className="text-gray-300" />
                        <span className="text-gray-900 font-black">Blog</span>
                    </div>
                </div>
            </div>

            <WhatToRead data={blogFeaturedData} />

            <section className="pb-16">
                <AdvertisementSection />
            </section>

            <MoreNews />

            <Footer />
        </main>
    );
}
