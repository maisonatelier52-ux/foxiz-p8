import React from 'react';
import StripCard from '../cards/StripCard';
import stripData from '@/public/data/news-strip.json';

export default function NewsStrip() {
    return (
        <section className="w-full bg-white py-8 border-t border-gray-100">
            <div className="max-w-[1330px] mx-auto px-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
                    {stripData.items.map((item, index) => (
                        <StripCard key={index} {...item} />
                    ))}
                </div>
            </div>
        </section>
    );
}
