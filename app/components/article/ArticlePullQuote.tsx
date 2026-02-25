import React from 'react';

export default function ArticlePullQuote({ quote, author }: { quote: string, author: string }) {
    return (
        <div className="my-12 flex flex-col items-center text-center">
            <span className="text-red-500 text-6xl font-serif italic mb-2 leading-none">"</span>
            <blockquote className="max-w-2xl">
                <p className="text-2xl md:text-3xl font-extrabold text-[#09365E] leading-tight mb-4">
                    {quote}
                </p>
                <footer className="flex items-center justify-center gap-3">
                    <div className="w-8 h-[2px] bg-red-600"></div>
                    <cite className="not-italic text-sm font-bold text-gray-500 uppercase tracking-widest italic font-serif">
                        {author}
                    </cite>
                </footer>
            </blockquote>
        </div>
    );
}
